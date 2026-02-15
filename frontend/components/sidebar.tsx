
"use client";

import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import { ScrollArea } from "@/components/ui/scroll-area";
import { FileText, Image, Film, LayoutGrid } from "lucide-react";

interface SidebarProps extends React.HTMLAttributes<HTMLDivElement> {
    onSelectCategory: (category: string) => void;
    selectedCategory: string;
}

export function Sidebar({ className, onSelectCategory, selectedCategory }: SidebarProps) {
    const categories = [
        { name: "Characters", id: "characters", icon: FileText },
        { name: "Environments", id: "environments", icon: LayoutGrid },
        // { name: "Styles", id: "styles", icon: LayoutGrid }, // Styles might be handled differently
        { name: "Gallery", id: "gallery", icon: Image },
    ];

    return (
        <div className={cn("pb-12 w-64 border-r", className)}>
            <div className="space-y-4 py-4">
                <div className="px-3 py-2">
                    <h2 className="mb-2 px-4 text-lg font-semibold tracking-tight">
                        Move 37
                    </h2>
                    <div className="space-y-1">
                        {categories.map((category) => (
                            <Button
                                key={category.id}
                                variant={selectedCategory === category.id ? "secondary" : "ghost"}
                                className="w-full justify-start"
                                onClick={() => onSelectCategory(category.id)}
                            >
                                <category.icon className="mr-2 h-4 w-4" />
                                {category.name}
                            </Button>
                        ))}
                    </div>
                </div>
            </div>
        </div>
    );
}
