"use client";

import * as TabsPrimitive from "@radix-ui/react-tabs";

import { cn } from "@/lib/utils";

export const Tabs = TabsPrimitive.Root;

export function TabsList({ className, ...props }: TabsPrimitive.TabsListProps): JSX.Element {
  return <TabsPrimitive.List className={cn("inline-flex rounded-lg bg-slate-100 p-1", className)} {...props} />;
}

export function TabsTrigger({ className, ...props }: TabsPrimitive.TabsTriggerProps): JSX.Element {
  return (
    <TabsPrimitive.Trigger
      className={cn(
        "rounded-md px-3 py-1.5 text-sm text-slate-600 data-[state=active]:bg-white data-[state=active]:text-slate-900",
        className
      )}
      {...props}
    />
  );
}

export function TabsContent({ className, ...props }: TabsPrimitive.TabsContentProps): JSX.Element {
  return <TabsPrimitive.Content className={cn("mt-4", className)} {...props} />;
}
