import React, { JSX } from "react";

interface Column<T> {
  header: string;
  accessor: keyof T;
}

interface ClickableTableProps<T> {
  data: T[];
  columns: Column<T>[];
  onRowClick: (row: T) => void;
}

const ClickableTable = <T,>({
  data,
  columns,
  onRowClick,
}: ClickableTableProps<T>): JSX.Element => {
  return (
    <table style={{ width: "100%", borderCollapse: "collapse" }}>
      <thead>
        <tr>
          {columns.map((col, index) => (
            <th
              key={index}
              style={{
                border: "1px solid #ccc",
                padding: "8px",
                textAlign: "left",
                background: "#f0f0f0",
              }}
            >
              {col.header}
            </th>
          ))}
        </tr>
      </thead>
      <tbody>
        {data.map((row, rowIndex) => (
          <tr
            key={rowIndex}
            onClick={() => onRowClick(row)}
            style={{ cursor: "pointer", border: "1px solid #ccc" }}
          >
            {columns.map((col, colIndex) => (
              <td
                key={colIndex}
                style={{ border: "1px solid #ccc", padding: "8px" }}
              >
                {row[col.accessor] as React.ReactNode}
              </td>
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  );
};

export default ClickableTable;
