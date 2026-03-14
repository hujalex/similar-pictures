"use client";

import { PreviewMessage, ThinkingMessage } from "@/components/message";
import { MultimodalInput } from "@/components/multimodal-input";
import { useScrollToBottom } from "@/hooks/use-scroll-to-bottom";
import { useChat, type UIMessage } from "@ai-sdk/react";
import { toast } from "sonner";

import React, { useRef } from "react";
import { motion } from "framer-motion";
import { processImage } from "@/lib/actions/image.actions";
import { Skeleton } from "@/components/ui/skeleton";

export function Dashboard() {
  const chatId = "001";
  const fileInputRef = useRef<HTMLInputElement>(null);

  const { messages, setMessages, sendMessage, status, stop } = useChat({
    id: chatId,
    onError: (error: Error) => {
      if (error.message.includes("Too many requests")) {
        toast.error(
          "You are sending too many messages. Please try again later.",
        );
      }
    },
  });

  const [messagesContainerRef, messagesEndRef] =
    useScrollToBottom<HTMLDivElement>();

  const [input, setInput] = React.useState("");
  const [selectedFile, setSelectedFile] = React.useState<string | null>(null);

  const isLoading = status === "submitted" || status === "streaming";

  const handleSubmit = (event?: { preventDefault?: () => void }) => {
    event?.preventDefault?.();
    if (input.trim()) {
      sendMessage({ text: input });
      setInput("");
    }
  };

  const handleFileSelect = async (
    event: React.ChangeEvent<HTMLInputElement>,
  ) => {
    try {
      const file = event.target.files?.[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = async (e) => {
          const dataUrl = e.target?.result as string;
          setSelectedFile(dataUrl);
          // sendMessage({
          //   role: "user",
          //   parts: [
          //     {
          //       type: "image" as "text",
          //       image: dataUrl,
          //     },
          //   ] as any,
          // });
          await processImage(dataUrl);
          toast.success("Image uploaded! Finding similar paintings...");
        };
        reader.readAsDataURL(file);
      }
    } catch (error) {
      console.error("Unable to Upload Image", error);
      toast.error("Unable to Upload Image");
    }
  };

  const handleEaselClick = () => {
    fileInputRef.current?.click();
  };

  return (
    <div className="relative flex flex-col min-w-0 h-[calc(100dvh-52px)] overflow-hidden">
      {/* WikiArt-inspired clean background */}
      <div className="absolute inset-0 bg-[#f8f9fa]">
        {/* Subtle grid pattern */}
        <div
          className="absolute inset-0 opacity-30"
          style={{
            backgroundImage: `
              linear-gradient(rgba(26,33,39,0.03) 1px, transparent 1px),
              linear-gradient(90deg, rgba(26,33,39,0.03) 1px, transparent 1px)
            `,
            backgroundSize: "40px 40px",
          }}
        />
      </div>

      {/* Top accent bar */}
      <div className="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-[#0057a7] via-[#eda000] to-[#0057a7]" />

      <motion.div
        ref={messagesContainerRef}
        className="relative flex flex-col min-w-0 gap-6 flex-1 overflow-y-scroll pt-8 px-4"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.5 }}
      >
        {/* Clean upload card - WikiArt style */}
        {!selectedFile && messages.length === 0 && (
          <motion.div
            className="flex justify-center"
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, ease: "easeOut" }}
          >
            {/* Hidden file input */}
            <input
              ref={fileInputRef}
              type="file"
              accept="image/*"
              onChange={handleFileSelect}
              className="hidden"
            />

            {/* Clean card with hover effect */}
            <motion.div
              className="relative w-full max-w-lg"
              onClick={handleEaselClick}
              whileHover={{ y: -4 }}
              transition={{ type: "spring", stiffness: 300, damping: 20 }}
            >
              {/* Card shadow */}
              <div className="absolute inset-0 bg-[#1a2127] rounded-xl translate-y-3 opacity-10" />

              {/* Main card */}
              <div className="relative bg-white rounded-xl border border-[#e7ebef] shadow-sm hover:shadow-lg transition-shadow duration-300 overflow-hidden">
                {/* Top gradient accent */}
                <div className="h-1 bg-gradient-to-r from-[#0057a7] to-[#eda000]" />

                <div className="p-8">
                  {/* Icon */}
                  <motion.div
                    className="w-16 h-16 mx-auto mb-6 rounded-full bg-[#f3f5f7] flex items-center justify-center"
                    whileHover={{ scale: 1.05, backgroundColor: "#e7ebef" }}
                  >
                    <svg
                      className="w-8 h-8 text-[#0057a7]"
                      fill="none"
                      viewBox="0 0 24 24"
                      stroke="currentColor"
                      strokeWidth={1.5}
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        d="M2.25 15.75l5.159-5.159a2.25 2.25 0 013.182 0l5.159 5.159m-1.5-1.5l1.409-1.409a2.25 2.25 0 013.182 0l2.909 2.909m-18 3.75h16.5a1.5 1.5 0 001.5-1.5V6a1.5 1.5 0 00-1.5-1.5H3.75A1.5 1.5 0 002.25 6v12a1.5 1.5 0 001.5 1.5zm10.5-11.25h.008v.008h-.008V8.25zm.375 0a.375.375 0 11-.75 0 .375.375 0 01.75 0z"
                      />
                    </svg>
                  </motion.div>

                  {/* Text */}
                  <div className="text-center">
                    <motion.h2
                      className="text-xl font-medium text-[#1a2127] mb-2"
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 1 }}
                      transition={{ delay: 0.2 }}
                    >
                      Find Similar Paintings
                    </motion.h2>
                    <motion.p
                      className="text-[#a4a4a4] text-sm"
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 1 }}
                      transition={{ delay: 0.3 }}
                    >
                      Upload an artwork to discover similar masterpieces
                    </motion.p>
                  </div>

                  {/* Upload button */}
                  <motion.button
                    className="mt-6 w-full py-3 px-6 bg-[#0057a7] text-white rounded-lg font-medium text-sm hover:bg-[#004a8f] transition-colors flex items-center justify-center gap-2"
                    whileHover={{ scale: 1.02 }}
                    whileTap={{ scale: 0.98 }}
                  >
                    <svg
                      className="w-4 h-4"
                      fill="none"
                      viewBox="0 0 24 24"
                      stroke="currentColor"
                      strokeWidth={2}
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        d="M3 16.5v2.25A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75V16.5m-13.5-9L12 3m0 0l4.5 4.5M12 3v13.5"
                      />
                    </svg>
                    Upload Image
                  </motion.button>

                  {/* Supported formats */}
                  <motion.p
                    className="mt-3 text-xs text-[#a4a4a4] text-center"
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ delay: 0.4 }}
                  >
                    Supports JPG, PNG, WEBP up to 10MB
                  </motion.p>
                </div>
              </div>
            </motion.div>
          </motion.div>
        )}

        {/* Selected image preview */}
        {selectedFile && messages.length === 0 && (
          <motion.div
            className="flex justify-center"
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
          >
            <div className="relative">
              <img
                src={selectedFile}
                alt="Selected"
                className="max-h-64 rounded-lg shadow-lg border border-[#e7ebef]"
              />
              <motion.button
                className="absolute -top-2 -right-2 w-8 h-8 bg-red-500 text-white rounded-full flex items-center justify-center shadow-md"
                whileHover={{ scale: 1.1 }}
                whileTap={{ scale: 0.9 }}
                onClick={() => setSelectedFile(null)}
              >
                <svg
                  className="w-4 h-4"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                  strokeWidth={2}
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    d="M6 18L18 6M6 6l12 12"
                  />
                </svg>
              </motion.button>
            </div>
          </motion.div>
        )}

        {/* 2x5 Grid of Skeleton cards (loading state) */}
        {selectedFile && (
          <div className="grid grid-cols-5 gap-4 max-w-5xl mx-auto mt-8 px-4">
            {Array.from({ length: 10 }).map((_, index) => (
              <div
                key={index}
                className="relative"
                style={{ paddingBottom: "140%" }}
              >
                <Skeleton className="absolute inset-0 rounded-lg" />
              </div>
            ))}
          </div>
        )}

        {/* Messages */}
        <>
          {messages.map((message: UIMessage, index: number) => (
            <motion.div
              key={message.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.4 }}
              layout
            >
              <PreviewMessage
                chatId={chatId}
                message={message}
                isLoading={isLoading && messages.length - 1 === index}
              />
            </motion.div>
          ))}
        </>

        {isLoading &&
          messages.length > 0 &&
          messages[messages.length - 1].role === "user" && (
            <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
              <ThinkingMessage />
            </motion.div>
          )}

        <div
          ref={messagesEndRef}
          className="shrink-0 min-w-[24px] min-h-[24px]"
        />
      </motion.div>

      {/* Clean input area */}
      <motion.div
        className="relative px-4 pb-4 md:pb-6"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3 }}
      >
        {/* Subtle top border */}
        <div className="absolute top-0 left-0 right-0 h-px bg-gradient-to-r from-transparent via-[#e7ebef] to-transparent" />

        {/* <form className="relative flex mx-auto gap-2 w-full md:max-w-3xl pt-4">
          <div className="flex-1 relative">
            {/* Clean border effect */}
        {/* <div className="absolute -inset-0.5 rounded-xl bg-gradient-to-r from-[#0057a7]/0 via-[#0057a7]/10 to-[#0057a7]/0 opacity-0 focus-within:opacity-100 transition-opacity" />
            <MultimodalInput
              chatId={chatId}
              input={input}
              setInput={setInput}
              handleSubmit={handleSubmit}
              isLoading={isLoading}
              stop={stop}
              messages={messages}
              setMessages={setMessages}
              sendMessage={sendMessage}
            />
          </div> */}
        {/* </form> */}
      </motion.div>
    </div>
  );
}
