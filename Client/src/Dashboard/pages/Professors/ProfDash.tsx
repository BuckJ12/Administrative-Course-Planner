import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import ClickableTable from '@/Shared/components/ClickableTable';
import ProfService from '@/Services/profService';
import { professor } from '@/types/professorTypes';
import { toast } from 'react-toastify';
import CreateButton from '@/Shared/components/CreateButton';

function ProfDash() {
  const [Professor, setProfessor] = useState<professor[]>([]);
  const navigate = useNavigate();

  const columns = [
    { title: 'Name', field: 'name' },
    { title: 'Max Workload', field: 'max_credit_hours' },
    {
      title: 'Courses',
      field: 'courses',
      render: (rowData: any) =>
        Array.isArray(rowData.courses)
          ? rowData.courses.map((course: any) => course.name).join(', ')
          : rowData.courses.name,
    },
  ];

  useEffect(() => {
    const fetchData = async () => {
      const data = await ProfService.getAll();
      console.log(data);
      setProfessor(data);
    };
    fetchData();
  }, []);

  const handleRowClick = (row: professor) => {
    navigate(`/professor/${row.id}`);
  };

  const deleteProfessor = async (id: number) => {
    await ProfService.delete(id);
  };

  const handleDeleteClick = async (p: professor) => {
    const originalprofs = [...Professor];
    try {
      setProfessor(Professor.filter((Professor) => Professor.id !== p.id));
      await deleteProfessor(p.id);
      toast.success('Professor deleted successfully');
      // eslint-disable-next-line @typescript-eslint/no-unused-vars
    } catch (error) {
      setProfessor(originalprofs);
      toast.error('Error deleting Professor, please try again');
    }
  };

  return (
    <>
      <h1 className='flex justify-center align-items-center'>
        Professor
        <CreateButton
          handleClick={() => navigate('/professors/add')}
        ></CreateButton>
      </h1>
      <ClickableTable
        columns={columns}
        data={Professor}
        onRowClick={handleRowClick}
        onRowDelete={handleDeleteClick}
        deleteModalRenderer={undefined}
      />
    </>
  );
}
export default ProfDash;
