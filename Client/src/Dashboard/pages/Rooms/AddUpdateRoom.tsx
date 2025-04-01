import useForm from '@/Shared/hooks/useForm';
import Joi from 'joi';
import { toast } from 'react-toastify';
import { useNavigate } from 'react-router-dom';
import { useParams } from 'react-router-dom';
import { useState } from 'react';
import RoomService from '@/Services/roomService';
import { roomDTO } from '@/types/roomTypes';
import Loading from '@/Shared/components/Loading';
import { useEffect } from 'react';

interface FormProps {
  name: string;
  capacity: number;
}

function AddUpdateRoom() {
  const { id } = useParams();
  const parsedId = id ? parseInt(id, 10) : undefined;
  const isUpdateMode = parsedId !== undefined;
  const Message = isUpdateMode ? 'Update Room' : 'Add Room';
  const [isLoading, setIsLoading] = useState(isUpdateMode);
  const Navigate = useNavigate();
  const fields: FormProps = {
    name: '',
    capacity: 0,
  };

  const schema = Joi.object({
    name: Joi.string().required().label('Name'),
    capacity: Joi.number().required().label('Capacity'),
  });

  useEffect(() => {
    if (isUpdateMode) {
      loadParsedData(parsedId!).then(() => setIsLoading(false));
    }
  }, [parsedId]);

  const loadParsedData = async (parseId: number) => {
    const course = await RoomService.getById(parseId);
    form.setData({
      name: course.name,
      capacity: course.capacity,
    });
  };

  async function doSubmit() {
    try {
      const NewRoom: roomDTO = {
        name: form.data.name,
        capacity: form.data.capacity,
      };
      if (isUpdateMode) {
        await RoomService.update(parsedId!, NewRoom);
        toast.success('Room Updated Successfully');
      } else {
        await RoomService.create(NewRoom);
        toast.success('Room Created Successfully');
      }
      Navigate('/rooms');
    } catch {
      toast.error('An unexpected error occurred.');
    }
  }

  const form = useForm<FormProps>({ fields, schema, doSubmit });

  if (isLoading) return <Loading />;

  return (
    <>
      <h1> {Message} </h1>
      {form.renderInput({ id: 'name', label: 'Name', type: 'string' })}
      {form.renderInput({
        id: 'capacity',
        label: 'Capacity',
        type: 'number',
      })}

      {form.renderButton(isUpdateMode ? 'Update' : 'Create')}
    </>
  );
}

export default AddUpdateRoom;
