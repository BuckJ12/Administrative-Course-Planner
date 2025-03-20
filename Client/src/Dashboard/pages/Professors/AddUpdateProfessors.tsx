import useForm from '@/Shared/hooks/useForm';
import { courses } from '@/types/courseTypes';
import { profDTO } from '@/types/professorTypes';
import ReactiveSearchWithTable from '@/Shared/components/ReactiveSearchWithTable';
import Joi from 'joi';
import { toast } from 'react-toastify';
import { useEffect } from 'react';
import ProfService from '@/Services/profService';
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import CourseService from '@/Services/courseService';
import Loading from '@/Shared/components/Loading';
import { useParams } from 'react-router-dom';

interface FormProps {
  name: string;
  max_credit_hours: number;
  courses: courses[];
}

function AddUpdateProfessor() {
  const [courses, setCourses] = useState<courses[]>([]);
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
  };

  useEffect(() => {
    const fetchData = async () => {
      const data = await CourseService.getAll();
      setCourses(data);
    };
    fetchData();
  }, []);

  const schema = Joi.object({
    name: Joi.string().required().label('Name'),
    max_credit_hours: Joi.number().required().min(1).label('Max Credits'),
    courses: Joi.array().label('Courses'),
  });

  useEffect(() => {
    if (isUpdateMode) {
      loadParsedData(parsedId!).then(() => setIsLoading(false));
    }
  }, [parsedId]);

  const loadParsedData = async (parseId: number) => {
    const course = await ProfService.getById(parseId);
    form.setData({
      name: course.name,
      max_credit_hours: course.max_credit_hours,
      courses: course.courses,
    });
  };

  async function doSubmit() {
    try {
      const newProf: profDTO = {
        name: form.data.name,
        max_credit_hours: form.data.max_credit_hours,
        courses: form.data.courses.map((u) => u.id),
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

      {form.renderButton('Create')}
    </>
  );
}

export default AddUpdateProfessor;
