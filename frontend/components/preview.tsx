"use client";

import React, { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { generateCharacter, generateEnvironment, fetchAssets, fetchFiles, Asset } from "@/lib/api";
import { Loader2, Play } from "lucide-react";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Card } from "@/components/ui/card";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Label } from "@/components/ui/label";

interface PreviewProps {
    category: string;
    selectedFile: string | null;
}

export function Preview({ category, selectedFile }: PreviewProps) {
    const [generating, setGenerating] = useState(false);
    const [assets, setAssets] = useState<Asset[]>([]);
    const [styles, setStyles] = useState<string[]>([]);
    const [selectedStyle, setSelectedStyle] = useState<string>("default");

    const refreshAssets = () => {
        fetchAssets().then(setAssets).catch(console.error);
    }

    useEffect(() => {
        refreshAssets();
        // Load styles
        fetchFiles("styles").then((files) => {
            // Strip .json
            const styleIds = files.map(f => f.replace(".json", ""));
            setStyles(styleIds);
        }).catch(console.error);
    }, []);

    const handleRender = async () => {
        if (!selectedFile) return;
        setGenerating(true);
        try {
            // Strip extension for ID
            const id = selectedFile.replace(".json", "");

            if (category === "characters") {
                // Pass selected style if not default
                const styleArg = selectedStyle === "default" ? undefined : selectedStyle;
                await generateCharacter(id, styleArg, true);
            } else if (category === "environments") {
                await generateEnvironment(id, true);
            }
            refreshAssets();
        } catch (error) {
            console.error(error);
            alert("Generation failed Check console.");
        } finally {
            setGenerating(false);
        }
    };

    if (category === "gallery") {
        return (
            <div className="h-full flex flex-col p-4">
                <div className="flex justify-between items-center mb-4">
                    <h3 className="font-semibold text-lg">Gallery</h3>
                    <Button variant="outline" size="sm" onClick={refreshAssets}>Refresh</Button>
                </div>
                <ScrollArea className="flex-1">
                    <div className="grid grid-cols-2 lg:grid-cols-3 gap-4 pb-4">
                        {assets.map((asset, i) => (
                            <Card key={i} className="overflow-hidden bg-card">
                                <div className="aspect-square relative group">
                                    {asset.type === "video" ? (
                                        <video src={`http://localhost:8000${asset.path}`} controls className="w-full h-full object-cover" />
                                    ) : (
                                        <img
                                            src={`http://localhost:8000${asset.path}`}
                                            alt={asset.name}
                                            className="w-full h-full object-cover transition-all"
                                            loading="lazy"
                                        />
                                    )}
                                    <div className="absolute bottom-0 left-0 right-0 bg-black/60 p-1 text-xs text-white truncate opacity-0 group-hover:opacity-100 transition-opacity">
                                        {asset.name}
                                    </div>
                                </div>
                            </Card>
                        ))}
                    </div>
                </ScrollArea>
            </div>
        )
    }

    return (
        <div className="flex flex-col h-full bg-background border-l">
            <div className="p-4 border-b space-y-4 bg-muted/20">
                <div className="flex justify-between items-center">
                    <div>
                        <h3 className="font-medium">Preview / Render</h3>
                        <p className="text-xs text-muted-foreground">
                            {selectedFile ? `Target: ${selectedFile}` : "No file selected"}
                        </p>
                    </div>
                    <Button onClick={handleRender} disabled={generating || !selectedFile}>
                        {generating ? <Loader2 className="mr-2 h-4 w-4 animate-spin" /> : <Play className="mr-2 h-4 w-4" />}
                        Render
                    </Button>
                </div>

                {category === "characters" && (
                    <div className="flex items-center gap-2">
                        <Label htmlFor="style-select" className="text-xs whitespace-nowrap">Style Override:</Label>
                        <Select value={selectedStyle} onValueChange={setSelectedStyle}>
                            <SelectTrigger id="style-select" className="h-8">
                                <SelectValue placeholder="Select style" />
                            </SelectTrigger>
                            <SelectContent>
                                <SelectItem value="default">Default (from file)</SelectItem>
                                {styles.map(s => (
                                    <SelectItem key={s} value={s}>{s}</SelectItem>
                                ))}
                            </SelectContent>
                        </Select>
                    </div>
                )}
            </div>

            <div className="p-4 flex-1 overflow-hidden flex flex-col">
                <h4 className="mb-2 text-sm font-semibold text-muted-foreground">Latest Generation Results</h4>
                <ScrollArea className="flex-1 -mx-4 px-4">
                    <div className="grid grid-cols-2 gap-4 pb-4">
                        {assets
                            .filter(a => selectedFile ? a.name.includes(selectedFile.replace(".json", "")) : true)
                            // Sort by name desc (assuming timestamp or sequential naming) or just reverse
                            .slice(0, 6)
                            .map((asset, i) => (
                                <Card key={i} className="overflow-hidden bg-card">
                                    <div className="aspect-square relative cursor-pointer" onClick={() => window.open(`http://localhost:8000${asset.path}`, '_blank')}>
                                        <img
                                            src={`http://localhost:8000${asset.path}`}
                                            alt={asset.name}
                                            className="w-full h-full object-cover hover:opacity-90 transition-opacity"
                                        />
                                    </div>
                                </Card>
                            ))}
                    </div>
                    {assets.length === 0 && (
                        <div className="flex flex-col items-center justify-center h-40 text-muted-foreground text-sm border-2 border-dashed rounded-lg">
                            No assets found
                            <Button variant="link" onClick={refreshAssets} size="sm">Refresh</Button>
                        </div>
                    )}
                </ScrollArea>
            </div>
        </div>
    );
}
