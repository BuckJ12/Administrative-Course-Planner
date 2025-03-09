import useForm from '@/Shared/hooks/useForm';
import Joi from 'joi';
import { toast } from 'react-toastify';
import { useNavigate } from 'react-router-dom';
import RoomService from '@/Services/roomService';
import { roomDTO } from '@/types/roomTypes';

interface FormProps {
  name: string;
  capacity: number;
}

function AddProfessor() {
  const Navigate = useNavigate();
  const fields: FormProps = {
    name: '',
    capacity: 0,
  };

  const schema = Joi.object({
    name: Joi.string().required().label('Name'),
    max_credit_hours: Joi.number().required().min(1).label('Max Credits'),
    courses: Joi.array().label('Courses'),
  });

  async function doSubmit() {
    try {
      const NewRoom: roomDTO = {
        name: form.data.name,
        capacity: form.data.capacity,
      };
      await RoomService.create(NewRoom);
      console.log('Submit to api', NewRoom);
      toast.success('Course Created Successfully');
      Navigate('/courses');
    } catch {
      toast.error('An unexpected error occurred.');
    }
  }

  const form = useForm<FormProps>({ fields, schema, doSubmit });

  return (
    <>
      <h1> Add Room</h1>
      {form.renderInput({ id: 'name', label: 'Name', type: 'string' })}
      {form.renderInput({
        id: 'capacity',
        label: 'Capacity',
        type: 'number',
      })}
      {form.renderButton('Create')}
    </>
  );
}

export default AddProfessor;
