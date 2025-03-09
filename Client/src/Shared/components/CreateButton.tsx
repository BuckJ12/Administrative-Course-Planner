import { AiOutlinePlus } from 'react-icons/ai';
import HeaderButton from './HeaderButton';

interface CreateButtonProps {
  handleClick: () => void;
}

function CreateButton({ handleClick }: CreateButtonProps) {
  return (
    <HeaderButton
      handleClick={handleClick}
      text='Create'
      Icon={AiOutlinePlus}
    />
  );
}

export default CreateButton;
