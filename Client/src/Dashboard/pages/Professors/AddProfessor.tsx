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

interface FormProps {
  name: string;
  max_credit_hours: number;
  courses: courses[];
}

function AddProfessor() {
  const [courses, setCourses] = useState<courses[]>([]);
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

  async function doSubmit() {
    try {
      const newProf: profDTO = {
        name: form.data.name,
        max_credit_hours: form.data.max_credit_hours,
        courses: form.data.courses.map((u) => u.id),
      };
      await ProfService.create(newProf);
      console.log('Submit to api', newProf);
      toast.success('Professor Created Successfully');
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

  return (
    <>
      <h1> Add Professor</h1>
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

export default AddProfessor;
