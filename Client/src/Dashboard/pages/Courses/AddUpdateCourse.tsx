import useForm from '@/Shared/hooks/useForm';
import { courseDTO } from '@/types/courseTypes';
import { professor } from '@/types/professorTypes';
import courseService from '@/Services/courseService';
import ReactiveSearchWithTable from '@/Shared/components/ReactiveSearchWithTable';
import Joi from 'joi';
import { toast } from 'react-toastify';
import { useEffect } from 'react';
import ProfService from '@/Services/profService';
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useParams } from 'react-router-dom';
import Loading from '@/Shared/components/Loading';

interface FormProps {
  name: string;
  credits: number;
  days: string;
  sections: number;
  slots_needed: number;
  max_students: number;
  professors: professor[];
}

function AddUpdateCourse() {
  const [professors, setProfessors] = useState<professor[]>([]);
  const { id } = useParams();
  const parsedId = id ? parseInt(id, 10) : undefined;
  const isUpdateMode = parsedId !== undefined;
  const Message = isUpdateMode ? 'Update Course' : 'Add Course';
  const [isLoading, setIsLoading] = useState(isUpdateMode);
  const Navigate = useNavigate();
  const fields: FormProps = {
    name: '',
    credits: 0,
    days: '',
    sections: 0,
    max_students: 0,
    professors: [],
    slots_needed: 0,
  };

  useEffect(() => {
    const fetchData = async () => {
      const data = await ProfService.getAll();
      setProfessors(data);
    };
    fetchData();
  }, []);

  const schema = Joi.object({
    name: Joi.string().required().label('Name'),
    credits: Joi.number().required().min(1).label('Credits'),
    days: Joi.string().required().label('Days'),
    sections: Joi.number().required().min(1).label('Sections'),
    max_students: Joi.number().required().min(1).label('Max Students'),
    professors: Joi.array().label('Professors'),
    slots_needed: Joi.number().min(1).label('Slots Needed'),
  });

  useEffect(() => {
    if (isUpdateMode) {
      loadParsedData(parsedId!).then(() => setIsLoading(false));
    }
  }, [parsedId]);

  const loadParsedData = async (parseId: number) => {
    const course = await courseService.getById(parseId);
    form.setData({
      name: course.name,
      credits: course.credit_hours,
      days: course.meeting_days,
      sections: course.number_of_sections,
      max_students: course.max_students,
      professors: course.professors,
      slots_needed: course.slots_needed,
    });
  };

  async function doSubmit() {
    try {
      const newCourse: courseDTO = {
        name: form.data.name,
        credit_hours: form.data.credits,
        meeting_Days: form.data.days,
        numberOfSections: form.data.sections,
        max_students: form.data.max_students,
        slots_needed: form.data.slots_needed,
        professors: form.data.professors.map((u) => u.id),
      };
      if (isUpdateMode) {
        await courseService.update(parsedId!, newCourse);
        toast.success('Course Updated Successfully');
      } else {
        await courseService.create(newCourse);
        toast.success('Course Created Successfully');
      }
      Navigate('/courses');
    } catch {
      toast.error('An unexpected error occurred.');
    }
  }

  const handleProfSelect = (professor: professor) => {
    const Newprofs = [...form.data.professors, professor];
    form.handleDataChange('professors', Newprofs);
  };

  const handleProfDelete = (id: number) => {
    const Newprofs = form.data.professors.filter((u) => u.id !== id);
    form.handleDataChange('professors', Newprofs);
  };

  const form = useForm<FormProps>({ fields, schema, doSubmit });

  const ProfOptions = professors.filter(
    (prof) =>
      !form.data.professors.some((selectedProf) => selectedProf.id === prof.id)
  );

  if (isLoading) return <Loading />;

  return (
    <>
      <h1> {Message}</h1>
      {form.renderInput({ id: 'name', label: 'Name', type: 'string' })}
      {form.renderInput({
        id: 'credits',
        label: 'Credit Hours',
        type: 'number',
      })}
      {form.renderSelect('days', 'Days the Class meets', [
        { value: 'MWF', name: 'MWF' },
        { value: 'TTH', name: 'TTH' },
      ])}
      {form.renderInput({
        id: 'sections',
        label: 'Number Of Sections',
        type: 'number',
      })}
      {form.renderInput({
        id: 'max_students',
        label: 'Max Students',
        type: 'number',
      })}
      {form.renderInput({
        id: 'slots_needed',
        label: 'Time Blocks Needed',
        type: 'number',
      })}
      <ReactiveSearchWithTable
        tableHeaderName='Professors'
        id='professors'
        classStyle=''
        selectedItems={form.data.professors}
        options={ProfOptions}
        selectionLabel='Select Professors'
        error={form.errors.professors}
        handleSelect={handleProfSelect}
        handleDelete={handleProfDelete}
      />

      {form.renderButton(isUpdateMode ? 'Update' : 'Create')}
    </>
  );
}

export default AddUpdateCourse;
