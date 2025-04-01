import React from 'react';
import { FaTimes } from 'react-icons/fa';

interface IconCheckboxProps {
  checked: boolean;
  onClick: () => void;
}

const IconCheckbox: React.FC<IconCheckboxProps> = ({ checked, onClick }) => {
  return (
    <span
      onClick={onClick}
      style={{
        cursor: 'pointer',
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
