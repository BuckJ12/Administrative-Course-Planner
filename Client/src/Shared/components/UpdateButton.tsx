import { FaPencilAlt } from 'react-icons/fa';
import HeaderButton from './HeaderButton';

interface UpdateButtonProps {
  handleClick: () => void;
}

function UpdateButton({ handleClick }: UpdateButtonProps) {
  return (
    <HeaderButton handleClick={handleClick} text='Update' Icon={FaPencilAlt} />
  );
}

export default UpdateButton;
