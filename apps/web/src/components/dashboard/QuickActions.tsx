// Dashboard Components - QuickActions

import React from "react";
import Link from "next/link";
import { Card } from "@/components/common/Card";
import { Button } from "@/components/common/Button";

export const QuickActions: React.FC = () => {
  return (
    <Card>
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Link href="/projects/new" className="block">
          <div className="p-4 border-2 border-blue-100 rounded-lg hover:border-blue-500 hover:bg-blue-50 transition cursor-pointer">
            <div className="text-3xl mb-2">📋</div>
            <h3 className="font-semibold text-gray-900 text-sm">New Project</h3>
            <p className="text-xs text-gray-600 mt-1">Create a new project</p>
          </div>
        </Link>

        <Link href="/projects" className="block">
          <div className="p-4 border-2 border-green-100 rounded-lg hover:border-green-500 hover:bg-green-50 transition cursor-pointer">
            <div className="text-3xl mb-2">📊</div>
            <h3 className="font-semibold text-gray-900 text-sm">Quick Estimate</h3>
            <p className="text-xs text-gray-600 mt-1">Generate estimate fast</p>
          </div>
        </Link>

        <Link href="/upgrades" className="block">
          <div className="p-4 border-2 border-purple-100 rounded-lg hover:border-purple-500 hover:bg-purple-50 transition cursor-pointer">
            <div className="text-3xl mb-2">⭐</div>
            <h3 className="font-semibold text-gray-900 text-sm">Browse Upgrades</h3>
            <p className="text-xs text-gray-600 mt-1">See available options</p>
          </div>
        </Link>

        <Link href="/proposals" className="block">
          <div className="p-4 border-2 border-orange-100 rounded-lg hover:border-orange-500 hover:bg-orange-50 transition cursor-pointer">
            <div className="text-3xl mb-2">📄</div>
            <h3 className="font-semibold text-gray-900 text-sm">Create Proposal</h3>
            <p className="text-xs text-gray-600 mt-1">Generate professional</p>
          </div>
        </Link>
      </div>
    </Card>
  );
};
