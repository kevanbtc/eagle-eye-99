// Dashboard Components - StatsSummary

import React from "react";
import { DashboardStats } from "@/lib/types";
import { Card } from "@/components/common/Card";

interface StatsSummaryProps {
  stats: DashboardStats;
}

export const StatsSummary: React.FC<StatsSummaryProps> = ({ stats }) => {
  const statCards = [
    {
      label: "Total Projects",
      value: stats.totalProjects,
      subtext: "All time",
      color: "blue",
    },
    {
      label: "Pending Estimates",
      value: stats.pendingEstimates,
      subtext: "Awaiting review",
      color: "yellow",
    },
    {
      label: "Sent Proposals",
      value: stats.sentProposals,
      subtext: "This month",
      color: "purple",
    },
    {
      label: "Accepted",
      value: stats.acceptedProposals,
      subtext: "Funded projects",
      color: "green",
    },
  ];

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      {statCards.map((stat, idx) => (
        <Card key={idx}>
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">{stat.label}</p>
              <p className="mt-2 text-3xl font-bold text-gray-900">
                {stat.value}
              </p>
              <p className="mt-1 text-xs text-gray-500">{stat.subtext}</p>
            </div>
            <div
              className={`w-12 h-12 rounded-lg flex items-center justify-center text-2xl ${
                stat.color === "blue"
                  ? "bg-blue-100 text-blue-600"
                  : stat.color === "yellow"
                  ? "bg-yellow-100 text-yellow-600"
                  : stat.color === "purple"
                  ? "bg-purple-100 text-purple-600"
                  : "bg-green-100 text-green-600"
              }`}
            >
              {stat.color === "blue" && "📊"}
              {stat.color === "yellow" && "⏳"}
              {stat.color === "purple" && "📤"}
              {stat.color === "green" && "✅"}
            </div>
          </div>
        </Card>
      ))}
    </div>
  );
};
