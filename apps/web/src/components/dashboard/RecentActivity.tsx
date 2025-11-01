// Dashboard Components - RecentActivity

import React from "react";
import { Card } from "@/components/common/Card";

export const RecentActivity: React.FC = () => {
  const activities = [
    {
      id: 1,
      action: "Created estimate",
      project: "Downtown Office Complex",
      time: "2 hours ago",
      icon: "📊",
    },
    {
      id: 2,
      action: "Sent proposal",
      project: "Retail Store Renovation",
      time: "5 hours ago",
      icon: "📤",
    },
    {
      id: 3,
      action: "Project completed",
      project: "Residential Retrofit",
      time: "1 day ago",
      icon: "✅",
    },
    {
      id: 4,
      action: "Team member joined",
      project: "Sarah Johnson",
      time: "3 days ago",
      icon: "👤",
    },
  ];

  return (
    <Card title="Recent Activity">
      <div className="space-y-4">
        {activities.map((activity) => (
          <div
            key={activity.id}
            className="flex items-start space-x-4 pb-4 border-b border-gray-200 last:border-0 last:pb-0"
          >
            <div className="flex-shrink-0 text-2xl">{activity.icon}</div>
            <div className="flex-1 min-w-0">
              <p className="text-sm font-medium text-gray-900">
                {activity.action}
              </p>
              <p className="text-sm text-gray-500">{activity.project}</p>
              <p className="text-xs text-gray-400 mt-1">{activity.time}</p>
            </div>
          </div>
        ))}
      </div>
    </Card>
  );
};
