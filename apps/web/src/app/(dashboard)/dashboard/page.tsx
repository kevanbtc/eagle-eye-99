"use client";

import React, { useEffect, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { Card } from "@/components/common/Card";
import { Button } from "@/components/common/Button";
import { LoadingSpinner } from "@/components/common/LoadingSpinner";
import { DashboardLayout } from "@/components/layouts/DashboardLayout";
import { StatsSummary } from "@/components/dashboard/StatsSummary";
import { RecentActivity } from "@/components/dashboard/RecentActivity";
import { QuickActions } from "@/components/dashboard/QuickActions";
import { useAuth } from "@/hooks/useAuth";
import { useApi } from "@/hooks/useApi";
import { DashboardStats } from "@/lib/types";

export default function DashboardPage() {
  const router = useRouter();
  const { user, isAuthenticated, isLoading: authLoading } = useAuth();
  const { get } = useApi();
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    // Redirect to login if not authenticated
    if (!authLoading && !isAuthenticated) {
      router.push("/login");
    }
  }, [isAuthenticated, authLoading, router]);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        setLoading(true);
        const response = await get("/api/v1/dashboard/stats");
        if (response.success) {
          setStats(response.data);
        } else {
          setError(response.error || "Failed to load dashboard");
        }
      } catch (err) {
        setError("Error loading dashboard");
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    if (isAuthenticated && !authLoading) {
      fetchStats();
    }
  }, [isAuthenticated, authLoading, get]);

  if (authLoading || !isAuthenticated) {
    return <LoadingSpinner />;
  }

  if (loading) {
    return (
      <DashboardLayout>
        <LoadingSpinner />
      </DashboardLayout>
    );
  }

  return (
    <DashboardLayout>
      <div className="space-y-6">
        {/* Header */}
        <div className="flex flex-col md:flex-row md:items-center md:justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">
              Welcome back, {user?.firstName || "User"}!
            </h1>
            <p className="mt-1 text-gray-600">
              Here's what's happening with your projects today.
            </p>
          </div>
          <div className="mt-4 md:mt-0">
            <Link href="/projects/new">
              <Button variant="primary" size="lg">
                + New Project
              </Button>
            </Link>
          </div>
        </div>

        {/* Stats Summary */}
        {stats && <StatsSummary stats={stats} />}

        {/* Quick Actions */}
        <QuickActions />

        {/* Main Content Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Recent Projects - Takes up 2 columns */}
          <div className="lg:col-span-2">
            <Card title="Recent Projects" className="h-full">
              {stats && stats.recentProjects.length > 0 ? (
                <div className="space-y-4">
                  {stats.recentProjects.map((project) => (
                    <Link
                      key={project.id}
                      href={`/projects/${project.id}`}
                      className="flex items-center justify-between p-4 border border-gray-200 rounded-lg hover:border-blue-500 hover:bg-blue-50 transition"
                    >
                      <div>
                        <h3 className="font-semibold text-gray-900">
                          {project.name}
                        </h3>
                        <p className="text-sm text-gray-500">
                          {project.address}, {project.city}, {project.state}
                        </p>
                        <p className="text-sm text-gray-400 mt-1">
                          {project.squareFeet.toLocaleString()} sqft •{" "}
                          {project.buildingType}
                        </p>
                      </div>
                      <div className="text-right">
                        <span
                          className={`inline-block px-3 py-1 rounded-full text-xs font-medium ${
                            project.status === "completed"
                              ? "bg-green-100 text-green-800"
                              : project.status === "in-progress"
                              ? "bg-blue-100 text-blue-800"
                              : "bg-gray-100 text-gray-800"
                          }`}
                        >
                          {project.status.replace("-", " ").toUpperCase()}
                        </span>
                      </div>
                    </Link>
                  ))}
                </div>
              ) : (
                <div className="text-center py-12">
                  <p className="text-gray-500 mb-4">No projects yet</p>
                  <Link href="/projects/new">
                    <Button variant="secondary">Create First Project</Button>
                  </Link>
                </div>
              )}
            </Card>
          </div>

          {/* Activity Feed */}
          <div>
            <RecentActivity />
          </div>
        </div>

        {/* Getting Started */}
        {(!stats || stats.totalProjects === 0) && (
          <Card title="Getting Started" className="bg-gradient-to-r from-blue-50 to-indigo-50">
            <div className="space-y-4">
              <div className="flex items-start">
                <div className="flex-shrink-0">
                  <div className="flex items-center justify-center h-8 w-8 rounded-md bg-blue-600 text-white">
                    1
                  </div>
                </div>
                <div className="ml-4">
                  <h3 className="text-sm font-medium text-gray-900">
                    Create your first project
                  </h3>
                  <p className="mt-1 text-sm text-gray-600">
                    Start by entering your project details or uploading plans.
                  </p>
                </div>
              </div>
              <div className="flex items-start">
                <div className="flex-shrink-0">
                  <div className="flex items-center justify-center h-8 w-8 rounded-md bg-blue-600 text-white">
                    2
                  </div>
                </div>
                <div className="ml-4">
                  <h3 className="text-sm font-medium text-gray-900">
                    Generate an estimate
                  </h3>
                  <p className="mt-1 text-sm text-gray-600">
                    Our AI system will calculate costs automatically.
                  </p>
                </div>
              </div>
              <div className="flex items-start">
                <div className="flex-shrink-0">
                  <div className="flex items-center justify-center h-8 w-8 rounded-md bg-blue-600 text-white">
                    3
                  </div>
                </div>
                <div className="ml-4">
                  <h3 className="text-sm font-medium text-gray-900">
                    Create a professional proposal
                  </h3>
                  <p className="mt-1 text-sm text-gray-600">
                    Send funding-ready proposals to clients.
                  </p>
                </div>
              </div>
            </div>
          </Card>
        )}
      </div>
    </DashboardLayout>
  );
}
