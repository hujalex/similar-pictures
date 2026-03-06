"use client";

export const processImage = async (imageDataUrl: string) => {
  try {
    const response = await fetch("/api/upload-image", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ image: imageDataUrl }),
    });
    if (!response.ok) {
      throw new Error(response.statusText);
    }
  } catch (error) {
    console.error("Error processing image", error);
    throw error;
  }
};
