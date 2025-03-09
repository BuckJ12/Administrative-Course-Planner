import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import ClickableTable from '@/Shared/components/ClickableTable';
import ProfService from '@/Services/profService';
import { professor } from '@/types/professorTypes';
import { toast } from 'react-toastify';

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

  const handleDeleteClick = () => {
    toast('Feature Not Yet Implemented');
    // TODO: implement click functionality
  };

  return (
    <>
      <h1>Professor</h1>
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
