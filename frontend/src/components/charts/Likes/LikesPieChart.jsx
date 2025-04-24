import React, { useContext } from "react";
import { LikeContext } from "../../../context/like.context";
import { PieChart, ResponsiveContainer, Pie, Legend, Tooltip } from "recharts";

function LikesPieChart() {
  const { like } = useContext(LikeContext);

  if (!like || like.length === 0) {
    return <div>No data available for the chart.</div>;
  }

  return (
    <ResponsiveContainer width="100%" height="100%">
      <PieChart width={500} height={300}>
        <Pie
          data={like}
          dataKey="value"
          nameKey="key"
          cx="50%"
          cy="50%"
          outerRadius={80}
          fill="#8b5cf6"
        />
        <Tooltip />
        <Legend />
      </PieChart>
    </ResponsiveContainer>
  );
}

export default LikesPieChart;
