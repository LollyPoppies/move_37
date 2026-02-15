
"use client";

import { useState } from "react";
import { Sidebar } from "@/components/sidebar";
import { CodeEditor } from "@/components/editor";
import { Preview } from "@/components/preview";

export default function Home() {
  const [category, setCategory] = useState("characters");
  const [selectedFile, setSelectedFile] = useState<string | null>(null);

  // When category changes, reset selected file
  const handleCategoryChange = (newCategory: string) => {
    setCategory(newCategory);
    setSelectedFile(null); // Or logic to select first
  };

  return (
    <div className="flex h-screen w-full bg-background text-foreground overflow-hidden font-sans">
      <Sidebar
        className="flex-shrink-0"
        selectedCategory={category}
        onSelectCategory={handleCategoryChange}
      />
      <main className="flex flex-1 overflow-hidden">
        {/* Editor Panel (The Architect) */}
        {category !== "gallery" && (
          <div className="w-1/2 min-w-[400px] flex flex-col">
            <CodeEditor category={category} onFileSelect={setSelectedFile} />
          </div>
        )}

        {/* Preview Panel (The Cinema) */}
        <div className={`flex flex-col border-l border-border bg-muted/10 ${category === "gallery" ? "w-full" : "w-1/2"}`}>
          <Preview category={category} selectedFile={selectedFile} />
        </div>
      </main>
    </div>
  );
}
