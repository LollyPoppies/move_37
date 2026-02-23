
"use client";

import React, { useEffect, useState } from "react";
import Editor, { OnMount } from "@monaco-editor/react";
import { Button } from "@/components/ui/button";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { fetchFiles, readFile, saveFile, generateCharacterJson } from "@/lib/api";
import { Loader2, Save, Sparkles, Plus } from "lucide-react";
import { Input } from "@/components/ui/input";

interface CodeEditorProps {
    category: string; // 'characters' or 'environments'
    onFileSelect: (filename: string) => void;
}

export function CodeEditor({ category, onFileSelect }: CodeEditorProps) {
    const [files, setFiles] = useState<string[]>([]);
    const [selectedFile, setSelectedFile] = useState<string | null>(null);
    const [code, setCode] = useState<string>("");
    const [loading, setLoading] = useState(false);
    const [saving, setSaving] = useState(false);
    const [prompt, setPrompt] = useState("");
    const [generating, setGenerating] = useState(false);
    const [newFileName, setNewFileName] = useState("");
    const [isCreatingNew, setIsCreatingNew] = useState(false);

    useEffect(() => {
        if (category === "gallery") return;

        setLoading(true);
        fetchFiles(category)
            .then((data) => {
                setFiles(data);
                if (data.length > 0) {
                    // Don't auto-select to avoid overwriting state if user switches fast, 
                    // but for now let's auto-select first
                    handleFileChange(data[0]);
                } else {
                    setCode("");
                    setSelectedFile(null);
                }
            })
            .catch((err) => console.error(err))
            .finally(() => setLoading(false));
    }, [category]);

    const handleFileChange = async (filename: string) => {
        setSelectedFile(filename);
        onFileSelect(filename);
        setLoading(true);
        try {
            const data = await readFile(category, filename);
            setCode(data.content);
        } catch (error) {
            console.error(error);
            setCode("// Error loading file");
        } finally {
            setLoading(false);
        }
    };

    const handleSave = async () => {
        const filename = isCreatingNew ? (newFileName.endsWith(".json") ? newFileName : `${newFileName}.json`) : selectedFile;
        if (!filename) return;

        setSaving(true);
        try {
            await saveFile(category, filename, code);
            console.log("Saved!");
            if (isCreatingNew) {
                // Refresh list and select new file
                const updatedFiles = await fetchFiles(category);
                setFiles(updatedFiles);
                setSelectedFile(filename);
                setIsCreatingNew(false);
                setNewFileName("");
            }
        } catch (error) {
            console.error(error);
        } finally {
            setSaving(false);
        }
    };

    const handleGenerate = async () => {
        if (!prompt) return;
        setGenerating(true);
        try {
            const data = await generateCharacterJson(prompt);
            setCode(JSON.stringify(data, null, 4));
        } catch (error) {
            console.error(error);
        } finally {
            setGenerating(false);
        }
    };

    const handleStartCreateNew = () => {
        setIsCreatingNew(true);
        setSelectedFile(null);
        setCode(JSON.stringify({
            name: "New Character",
            physical_traits: {
                age_range: "",
                hair: "",
                eyes: "",
                physique: ""
            },
            clothing: "",
            extra_details: ""
        }, null, 4));
    };

    if (category === "gallery") {
        return <div className="p-4 text-muted-foreground">Select a category to edit files.</div>;
    }

    return (
        <div className="flex flex-col h-full border-r">
            <div className="p-4 border-b flex gap-2 items-center justify-between">
                <div className="flex gap-2 flex-1">
                    {!isCreatingNew ? (
                        <Select value={selectedFile || ""} onValueChange={handleFileChange}>
                            <SelectTrigger className="w-[200px]">
                                <SelectValue placeholder="Select a file" />
                            </SelectTrigger>
                            <SelectContent>
                                {files.map((f) => (
                                    <SelectItem key={f} value={f}>
                                        {f}
                                    </SelectItem>
                                ))}
                            </SelectContent>
                        </Select>
                    ) : (
                        <Input
                            value={newFileName}
                            onChange={(e) => setNewFileName(e.target.value)}
                            placeholder="filename.json"
                            className="w-[200px] h-9"
                        />
                    )}
                    {!isCreatingNew ? (
                        <Button variant="outline" size="sm" onClick={handleStartCreateNew}>
                            <Plus className="h-4 w-4 mr-1" /> New
                        </Button>
                    ) : (
                        <Button variant="ghost" size="sm" onClick={() => setIsCreatingNew(false)}>
                            Cancel
                        </Button>
                    )}
                </div>
                <Button size="sm" onClick={handleSave} disabled={saving || (!selectedFile && !newFileName)}>
                    {saving ? <Loader2 className="h-4 w-4 animate-spin" /> : <Save className="h-4 w-4" />}
                    <span className="sr-only">Save</span>
                </Button>
            </div>
            {category === "characters" && (
                <div className="p-4 border-b bg-muted/20 space-y-2">
                    <label className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">Generate from Prompt</label>
                    <div className="flex gap-2">
                        <Input
                            value={prompt}
                            onChange={(e) => setPrompt(e.target.value)}
                            placeholder="Describe a character (e.g. A cyberpunk samurai...)"
                            className="flex-1"
                        />
                        <Button size="sm" onClick={handleGenerate} disabled={generating || !prompt}>
                            {generating ? <Loader2 className="h-4 w-4 animate-spin" /> : <Sparkles className="h-4 w-4 mr-2" />}
                            Generate
                        </Button>
                    </div>
                </div>
            )}
            <div className="flex-1 min-h-0 bg-[#1e1e1e]">
                {/* Monaco Editor default theme is vs-dark which is #1e1e1e */}
                {loading ? (
                    <div className="flex items-center justify-center h-full text-muted-foreground">
                        <Loader2 className="h-6 w-6 animate-spin mr-2" /> Loading...
                    </div>
                ) : (
                    <Editor
                        height="100%"
                        defaultLanguage="json"
                        language="json"
                        value={code}
                        theme="vs-dark"
                        onChange={(value) => setCode(value || "")}
                        options={{
                            minimap: { enabled: false },
                            fontSize: 14,
                            scrollBeyondLastLine: false,
                            automaticLayout: true,
                        }}
                    />
                )}
            </div>
        </div>
    );
}
