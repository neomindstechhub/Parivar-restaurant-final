import { useRef, useState } from "react";
import { ImagePlus, Loader2, X } from "lucide-react";
import axios from "axios";
import { resolveImageUrl } from "@/utils/imageUrl";

interface ImageUploadFieldProps {
  value: string;
  onChange: (url: string) => void;
  label?: string;
}

export function ImageUploadField({ value, onChange, label = "Dish Image" }: ImageUploadFieldProps) {
  const inputRef = useRef<HTMLInputElement>(null);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState("");

  const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    if (!file.type.startsWith("image/")) {
      setError("Please select an image file.");
      return;
    }
    if (file.size > 5 * 1024 * 1024) {
      setError("Image must be smaller than 5MB.");
      return;
    }

    setError("");
    setUploading(true);
    try {
      const formData = new FormData();
      formData.append("file", file);
      const token = localStorage.getItem("parivar_admin_token");
      const res = await axios.post(
        (import.meta.env.VITE_API_URL || "http://localhost:8000") + "/api/v1/uploads/",
        formData,
        {
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "multipart/form-data",
          },
        },
      );
      onChange(res.data.url);
    } catch {
      setError("Failed to upload image. Please try again.");
    } finally {
      setUploading(false);
      if (inputRef.current) inputRef.current.value = "";
    }
  };

  return (
    <div>
      <label className="block text-sm font-medium mb-1">{label}</label>
      <div className="space-y-3">
        {value ? (
          <div className="relative w-full h-36 rounded-lg overflow-hidden border border-gray-200 bg-gray-50">
            <img
              src={resolveImageUrl(value)}
              alt="Dish preview"
              className="w-full h-full object-cover"
            />
            <button
              type="button"
              onClick={() => onChange("")}
              className="absolute top-2 right-2 p-1.5 rounded-full bg-black/50 text-white hover:bg-black/70 transition-colors"
              aria-label="Remove image"
            >
              <X className="w-4 h-4" />
            </button>
          </div>
        ) : (
          <button
            type="button"
            onClick={() => inputRef.current?.click()}
            disabled={uploading}
            className="w-full h-36 rounded-lg border-2 border-dashed border-gray-300 bg-gray-50 hover:border-[#0B5D3B] hover:bg-[#0B5D3B]/5 transition-colors flex flex-col items-center justify-center gap-2 text-gray-500 disabled:opacity-60"
          >
            {uploading ? (
              <>
                <Loader2 className="w-8 h-8 animate-spin text-[#0B5D3B]" />
                <span className="text-sm font-medium">Uploading...</span>
              </>
            ) : (
              <>
                <ImagePlus className="w-8 h-8 text-[#0B5D3B]" />
                <span className="text-sm font-medium">Click to upload image</span>
                <span className="text-xs text-gray-400">JPEG, PNG, WebP or GIF — max 5MB</span>
              </>
            )}
          </button>
        )}
        {value && (
          <button
            type="button"
            onClick={() => inputRef.current?.click()}
            disabled={uploading}
            className="text-sm text-[#0B5D3B] font-medium hover:underline disabled:opacity-60"
          >
            {uploading ? "Uploading..." : "Replace image"}
          </button>
        )}
        <input
          ref={inputRef}
          type="file"
          accept="image/jpeg,image/png,image/webp,image/gif"
          onChange={handleFileChange}
          className="hidden"
        />
        {error && <p className="text-xs text-red-600">{error}</p>}
      </div>
    </div>
  );
}
