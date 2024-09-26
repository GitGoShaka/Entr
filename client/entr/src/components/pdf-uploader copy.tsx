"use client"

import { useState, useRef } from "react"
import { Upload, File, X } from "lucide-react"
import { Button } from "@/components/ui/button"

export function PdfUploader() {
  const [file, setFile] = useState<File | null>(null)
  const [dragActive, setDragActive] = useState(false)
  const inputRef = useRef<HTMLInputElement>(null)

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true)
    } else if (e.type === "dragleave") {
      setDragActive(false)
    }
  }

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    setDragActive(false)
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFile(e.dataTransfer.files[0])
    }
  }

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    e.preventDefault()
    if (e.target.files && e.target.files[0]) {
      handleFile(e.target.files[0])
    }
  }

  const handleFile = (file: File) => {
    if (file.type === "application/pdf") {
      setFile(file)
    } else {
      alert("Please upload a PDF file")
    }
  }

  const onButtonClick = () => {
    inputRef.current?.click()
  }

  const handleUpload = async () => {
    if (file) {
      const formData = new FormData();
      formData.append('pdf', file);

      try {
        const response = await fetch('http://localhost:8080/api/upload-pdf', {
          method: 'POST',
          body: formData,
        });

        if (response.ok) {
          console.log('File uploaded successfully');
          setFile(null);
        } else {
          console.error('File upload failed');
        }
      } catch (error) {
        console.error('Error uploading file:', error);
      }
    }
  }

  return (
    <div className="max-w-xl mx-auto mt-8">
      <div 
        className={`relative p-12 border-2 border-dashed rounded-lg text-center ${
          dragActive ? "border-slate-900 dark:border-slate-50" : "border-gray-300"
        }`}
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
      >
        <input
          ref={inputRef}
          type="file"
          accept=".pdf"
          onChange={handleChange}
          className="hidden"
        />
        <Upload className="mx-auto h-12 w-12 text-gray-400" />
        <p className="mt-2 text-sm text-gray-600">Drag and drop your PDF here, or</p>
        <Button 
          type="button"
          variant="outline" 
          onClick={onButtonClick}
          className="mt-2"
        >
          Select PDF
        </Button>
        {file && (
          <div className="mt-4 flex items-center justify-center text-sm text-gray-600">
            <File className="mr-2 h-4 w-4" />
            {file.name}
            <button
              onClick={() => setFile(null)}
              className="ml-2 text-red-500 hover:text-red-700"
            >
              <X className="h-4 w-4" />
            </button>
          </div>
        )}
      </div>
      <Button 
        onClick={handleUpload} 
        disabled={!file}
        className="mt-4 w-full"
      >
        Upload PDF
      </Button>
    </div>
  )
}