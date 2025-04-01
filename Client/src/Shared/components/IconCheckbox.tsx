import React from 'react';
import { FaTimes } from 'react-icons/fa';

interface IconCheckboxProps {
  checked: boolean;
  onClick: () => void;
  readOnly?: boolean;
}

const IconCheckbox: React.FC<IconCheckboxProps> = ({
  checked,
  onClick,
  readOnly = false,
}) => {
  const handleClick = () => {
    if (!readOnly) {
      onClick();
    }
  };

  return (
    <span
      onClick={handleClick}
      style={{
        cursor: readOnly ? 'default' : 'pointer',
        display: 'flex',
        width: '20px',
        height: '20px',
        border: '1px solid #ccc',
        borderRadius: '3px',
        alignItems: 'center',
        justifyContent: 'center',
      }}
    >
      {checked && (
        <FaTimes style={{ color: 'red', width: '100%', height: '100%' }} />
      )}
    </span>
  );
};

export default IconCheckbox;
