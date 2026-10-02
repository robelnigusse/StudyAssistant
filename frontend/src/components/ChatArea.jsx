import React from 'react';
import { MenuIcon, PlusIcon, MessageIcon, BotIcon, LoaderIcon, SendIcon } from './icons/Icons';

export default function ChatArea({
  isSidebarOpen,
  setIsSidebarOpen,
  setCurrentConvId,
  messages,
  isLoading,
  input,
  setInput,
  handleSend,
  messagesEndRef
}) {
  const renderMessageContent = (content) => {
    return content.split('\n').map((line, idx) => (
      <React.Fragment key={idx}>
        {line}
        <br />
      </React.Fragment>
    ));
  };

  return (
    <div className="flex-1 flex flex-col h-full relative">
      {/* Header (visible when sidebar closed) */}
      {!isSidebarOpen && (
        <div className="absolute top-4 left-4 z-10">
          <button 
            onClick={() => setIsSidebarOpen(true)}
            className="p-2 hover:bg-[#2f2f2f] rounded-lg text-gray-400 hover:text-white transition-colors"
            title="Open sidebar"
          >
            <MenuIcon />
          </button>
        </div>
      )}

      {/* Header New Chat Button (Mobile/Compact) */}
      {!isSidebarOpen && (
          <div className="absolute top-4 right-4 z-10">
            <button 
              onClick={() => setCurrentConvId(null)}
              className="p-2 hover:bg-[#2f2f2f] rounded-lg text-gray-400 hover:text-white transition-colors"
              title="New chat"
            >
              <PlusIcon />
            </button>
          </div>
      )}

      <div className="flex-1 overflow-y-auto w-full flex justify-center scroll-smooth custom-scrollbar">
        {messages.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-full text-center px-4">
            <div className="w-16 h-16 bg-gradient-to-tr from-purple-500 to-blue-500 rounded-full flex items-center justify-center mb-6 shadow-lg shadow-purple-500/20">
              <MessageIcon className="w-8 h-8 text-white" />
            </div>
            <h1 className="text-3xl font-semibold mb-2 max-w-xl">Upload your books and get answers from them.</h1>
            <p className="text-gray-400 max-w-md">Start by uploading a PDF and then ask me anything about your course materials!</p>
          </div>
        ) : (
          <div className="w-full max-w-3xl flex flex-col pt-10">
            {messages.map((msg, idx) => (
              <div 
                key={msg.id || idx} 
                className={`flex w-full mb-6 px-4 ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div 
                  className={`max-w-[85%] sm:max-w-[75%] px-5 py-3 rounded-2xl ${
                    msg.role === 'user' 
                      ? 'bg-[#2f2f2f] text-white rounded-br-sm' 
                      : 'text-gray-100 bg-transparent'
                  }`}
                >
                  {msg.role === 'assistant' && (
                     <div className="flex items-center gap-2 mb-2 font-semibold text-purple-400 text-sm">
                        <div className="w-6 h-6 rounded-full bg-purple-500/20 flex items-center justify-center">
                          <BotIcon />
                        </div>
                        StudyAssistant
                     </div>
                  )}
                  <div className="leading-relaxed text-[15px] whitespace-pre-wrap">
                    {renderMessageContent(msg.content)}
                  </div>
                </div>
              </div>
            ))}
            {isLoading && (
              <div className="flex w-full mb-6 px-4 justify-start">
                <div className="max-w-[85%] sm:max-w-[75%] px-5 py-3">
                  <div className="flex items-center gap-2 mb-2 font-semibold text-purple-400 text-sm">
                      <div className="w-6 h-6 rounded-full bg-purple-500/20 flex items-center justify-center">
                        <BotIcon />
                      </div>
                      StudyAssistant
                  </div>
                  <div className="flex items-center gap-2 text-gray-400 py-2">
                     <LoaderIcon />
                     <span className="animate-pulse">Thinking...</span>
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>
        )}
      </div>

      {/* Input Area */}
      <div className="w-full bg-[#212121] pt-2 pb-6 px-4">
        <div className="max-w-3xl mx-auto relative">
          <form onSubmit={handleSend} className="relative flex items-end shadow-xl rounded-2xl bg-[#2f2f2f] border border-gray-700/50 focus-within:border-gray-500 transition-colors overflow-hidden">
            <textarea
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                  e.preventDefault();
                  handleSend(e);
                }
              }}
              placeholder="Message StudyAssistant..."
              className="w-full max-h-48 bg-transparent text-white pl-4 pr-12 py-4 focus:outline-none resize-none overflow-y-auto"
              rows="1"
              style={{ minHeight: '56px' }}
              onInput={(e) => {
                e.target.style.height = 'auto';
                e.target.style.height = e.target.scrollHeight + 'px';
              }}
            />
            <button 
              type="submit"
              disabled={!input.trim() || isLoading}
              className="absolute right-3 bottom-3 p-2 bg-white text-black hover:bg-gray-200 disabled:opacity-50 disabled:bg-gray-600 disabled:text-gray-400 disabled:hover:bg-gray-600 rounded-lg transition-all"
            >
              <SendIcon />
            </button>
          </form>
          <div className="text-center text-xs text-gray-500 mt-3">
            StudyAssistant can make mistakes. Consider verifying important information.
          </div>
        </div>
      </div>
    </div>
  );
}
