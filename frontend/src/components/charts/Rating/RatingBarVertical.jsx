import { useContext } from "react";
import { DataContext } from "../../../context/data.context";
import { RatingContext } from "../../../context/rating.context";
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

const BarChartComponent = () => {
  const { rating } = useContext(RatingContext);

  if (!rating || rating.length === 0) {
    return <p>No data available for the chart.</p>;
  }

  return (
    <ResponsiveContainer width="100%" height="100%">
      <BarChart
        width={500}
        height={300}
        data={rating}
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

export default BarChartComponent;

export const CustomTooltip = ({ active, payload, label }) => {
  if (active && payload && payload.length) {
    return (
      <div className="p-4 bg-slate-900 flex flex-col gap-4 rounded-md">
        <p className="text-sm text-blue-400">
          Value:
          <span className="ml-2"> {payload[0]?.value}</span>
        </p>
      </div>
    );
  }
  return null;
};
