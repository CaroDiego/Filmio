import React, { useContext } from "react";
import { YearContext } from "../../../context/year.context";
import { CustomTooltip } from "../Rating/RatingBarVertical";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";

const YearBarVertical = () => {
  const { year, groupedByDecade } = useContext(YearContext);

  if (!year || year.length === 0) {
    return <div>No data available for the chart.</div>;
  }

  const refinedData = Object.values(groupedByDecade);
  return (
    <ResponsiveContainer width="100%" height="100%">
      <BarChart
        width={500}
        height={300}
        data={refinedData}
        margin={{
          right: 30,
        }}
      >
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="key" />
        <YAxis />
        <Tooltip content={<CustomTooltip />} />
        <Legend />
        <Bar dataKey="value" fill="#8b5cf6" />
      </BarChart>
    </ResponsiveContainer>
  );
};

export default YearBarVertical;
