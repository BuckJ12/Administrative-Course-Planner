import useForm from '@/Shared/hooks/useForm';
import { courses } from '@/types/courseTypes';
import { profDTO } from '@/types/professorTypes';
import { useParams } from 'react-router-dom';
import { useNavigate } from 'react-router-dom';
import { toast } from 'react-toastify';
import { useEffect } from 'react';
import { useState } from 'react';
import ReactiveSearchWithTable from '@/Shared/components/ReactiveSearchWithTable';
import Joi from 'joi';
import ProfService from '@/Services/profService';
import CourseService from '@/Services/courseService';
import Loading from '@/Shared/components/Loading';
import TimeSlotsService from '@/Services/timeSlotsService';
import { timeSlot } from '@/types/timeTypes';
import TimeSlotChart from '@/Shared/components/TimeSlotChart';

interface FormProps {
  name: string;
  max_credit_hours: number;
  courses: courses[];
  selectedTimeSlots: number[];
}

function AddUpdateProfessor() {
  const [courses, setCourses] = useState<courses[]>([]);
  const [timeSlots, setTimeSlots] = useState<timeSlot[]>([]);
  const { id } = useParams();
  const parsedId = id ? parseInt(id, 10) : undefined;
  const isUpdateMode = parsedId !== undefined;
  const Message = isUpdateMode ? 'Update Professor' : 'Add Professor';
  const [isLoading, setIsLoading] = useState(isUpdateMode);
  const Navigate = useNavigate();
  const fields: FormProps = {
    name: '',
    max_credit_hours: 0,
    courses: [],
    selectedTimeSlots: [],
  };

  useEffect(() => {
    const fetchData = async () => {
      const data = await CourseService.getAll();
      const timeData = await TimeSlotsService.getAll();
      setTimeSlots(timeData);
      setCourses(data);
    };
    fetchData();
  }, []);

  const schema = Joi.object({
    name: Joi.string().required().label('Name'),
    max_credit_hours: Joi.number().required().min(1).label('Max Credits'),
    courses: Joi.array().label('Courses'),
    selectedTimeSlots: Joi.array().label('Time Slots'),
  });

  useEffect(() => {
    if (isUpdateMode) {
      loadParsedData(parsedId!).then(() => setIsLoading(false));
    }
  }, [parsedId]);

  const loadParsedData = async (parseId: number) => {
    const prof = await ProfService.getById(parseId);
    console.log(prof);
    form.setData({
      name: prof.name,
      max_credit_hours: prof.max_credit_hours,
      courses: prof.courses,
      selectedTimeSlots: prof.timeSlotRestrictions,
    });
  };

  async function doSubmit() {
    try {
      const newProf: profDTO = {
        name: form.data.name,
        max_credit_hours: form.data.max_credit_hours,
        courses: form.data.courses.map((u) => u.id),
        timeSlotRestrictions: form.data.selectedTimeSlots,
      };
      if (isUpdateMode) {
        await ProfService.update(parsedId!, newProf);
        toast.success('Professor Updated Successfully');
      } else {
        await ProfService.create(newProf);
        toast.success('Professor Created Successfully');
      }
      Navigate('/professors');
    } catch {
      toast.error('An unexpected error occurred.');
    }
  }

  const handleCourseSelect = (course: courses) => {
    const Newcourses = [...form.data.courses, course];
    form.handleDataChange('courses', Newcourses);
  };

  const handleCourseDelete = (id: number) => {
    const Newcourses = form.data.courses.filter((u) => u.id !== id);
    form.handleDataChange('courses', Newcourses);
  };

  const form = useForm<FormProps>({ fields, schema, doSubmit });

  const CourseOptions = courses.filter(
    (course) =>
      !form.data.courses.some(
        (Selectedcourse) => Selectedcourse.id === course.id
      )
  );

  const toggleTimeSelection = (id: number) => {
    if (form.data.selectedTimeSlots.includes(id)) {
      form.handleDataChange(
        'selectedTimeSlots',
        form.data.selectedTimeSlots.filter((item) => item !== id)
      );
    } else {
      form.handleDataChange('selectedTimeSlots', [
        ...form.data.selectedTimeSlots,
        id,
      ]);
    }
  };

  if (isLoading) return <Loading />;

  return (
    <>
      <h1> {Message}</h1>
      {form.renderInput({ id: 'name', label: 'Name', type: 'string' })}
      {form.renderInput({
        id: 'max_credit_hours',
        label: 'Max Credit Hours',
        type: 'number',
      })}

      <ReactiveSearchWithTable
        tableHeaderName='Courses'
        id='courses'
        classStyle=''
        selectedItems={form.data.courses}
        options={CourseOptions}
        selectionLabel='Select Courses'
        error={form.errors.courses}
        handleSelect={handleCourseSelect}
        handleDelete={handleCourseDelete}
      />

      <TimeSlotChart
        timeSlots={timeSlots}
        selectedIds={form.data.selectedTimeSlots}
        onToggle={toggleTimeSelection}
      />

      {form.renderButton(isUpdateMode ? 'Update' : 'Create')}
    </>
  );
}

export default AddUpdateProfessor;
