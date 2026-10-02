import React, { useRef } from 'react';
import { PlusIcon, MenuIcon, MessageIcon, TrashIcon, LoaderIcon, UploadIcon } from './icons/Icons';

export default function Sidebar({ 
  isSidebarOpen, 
  setIsSidebarOpen, 
  conversations, 
  currentConvId, 
  setCurrentConvId, 
  deleteConversation, 
  handleFileUpload, 
  isUploading 
}) {
  const fileInputRef = useRef(null);

  return (
    <div className={`transition-all duration-300 ease-in-out flex flex-col bg-[#171717] ${isSidebarOpen ? 'w-[260px] p-3' : 'w-0 p-0 overflow-hidden'} shrink-0 relative`}>
      <div className="flex gap-2 mb-6">
        <button 
          onClick={() => setCurrentConvId(null)}
          className="flex-1 flex items-center gap-2 px-3 py-2 bg-[#2f2f2f] hover:bg-[#3f3f3f] text-sm font-medium rounded-lg transition-colors"
        >
          <PlusIcon />
          New chat
        </button>
        <button 
          onClick={() => setIsSidebarOpen(false)}
          className="p-2 hover:bg-[#2f2f2f] rounded-lg text-gray-400 hover:text-white transition-colors"
          title="Close sidebar"
        >
          <MenuIcon />
        </button>
      </div>

      <div className="flex-1 overflow-y-auto space-y-1 custom-scrollbar">
        {conversations.map((conv) => (
          <div 
            key={conv.id}
            onClick={() => setCurrentConvId(conv.id)}
            className={`group flex items-center justify-between p-3 rounded-lg cursor-pointer transition-colors ${currentConvId === conv.id ? 'bg-[#2f2f2f]' : 'hover:bg-[#2f2f2f]'}`}
          >
            <div className="flex items-center gap-3 overflow-hidden text-sm">
              <MessageIcon />
              <span className="truncate">{conv.title || "New Conversation"}</span>
            </div>
            <button 
              onClick={(e) => deleteConversation(conv.id, e)}
              className="opacity-0 group-hover:opacity-100 text-gray-400 hover:text-red-400 p-1"
              title="Delete chat"
            >
              <TrashIcon />
            </button>
          </div>
        ))}
      </div>

      <div className="p-3 border-t border-gray-800">
        <input 
          type="file" 
          accept=".pdf" 
          ref={fileInputRef} 
          onChange={handleFileUpload} 
          className="hidden" 
        />
        <button 
          onClick={() => fileInputRef.current?.click()}
          disabled={isUploading}
          className="w-full flex items-center justify-center gap-2 px-3 py-2 bg-purple-600 hover:bg-purple-700 disabled:opacity-50 text-white text-sm font-medium rounded-lg transition-colors"
        >
          {isUploading ? <LoaderIcon /> : <UploadIcon />}
          {isUploading ? 'Uploading...' : 'Upload PDF'}
        </button>
      </div>
    </div>
  );
}
