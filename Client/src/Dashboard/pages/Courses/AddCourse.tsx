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

interface FormProps {
  name: string;
  credits: number;
  days: string;
  sections: number;
  max_students: number;
  professors: professor[];
}

function AddCourse() {
  const [professors, setProfessors] = useState<professor[]>([]);
  const Navigate = useNavigate();
  const fields: FormProps = {
    name: '',
    credits: 0,
    days: '',
    sections: 0,
    max_students: 0,
    professors: [],
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
  });

  async function doSubmit() {
    try {
      const newCourse: courseDTO = {
        name: form.data.name,
        credit_hours: form.data.credits,
        meeting_Days: form.data.days,
        numberOfSections: form.data.sections,
        max_students: form.data.max_students,
        professors: form.data.professors.map((u) => u.id),
      };
      await courseService.create(newCourse);
      console.log('Submit to api', newCourse);
      toast.success('Course Created Successfully');
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
    console.log('delete', id);
    const Newprofs = form.data.professors.filter((u) => u.id !== id);
    console.log(Newprofs);
    form.handleDataChange('professors', Newprofs);
  };

  const form = useForm<FormProps>({ fields, schema, doSubmit });

  const ProfOptions = professors.filter(
    (prof) =>
      !form.data.professors.some((selectedProf) => selectedProf.id === prof.id)
  );

  return (
    <>
      <h1> Add Course</h1>
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

      {form.renderButton('Create')}
    </>
  );
}

export default AddCourse;
