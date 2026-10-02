import React, { useEffect, useState } from 'react';
import { CloseIcon, TrashIcon, BookIcon, LoaderIcon } from './icons/Icons';

const API_BASE_URL = 'http://127.0.0.1:8000';

export default function BooksModal({ isOpen, onClose }) {
  const [books, setBooks] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    if (isOpen) {
      fetchBooks();
    }
  }, [isOpen]);

  const fetchBooks = async () => {
    setIsLoading(true);
    try {
      const res = await fetch(`${API_BASE_URL}/books/`);
      if (res.ok) {
        const data = await res.json();
        setBooks(data.books || []);
      }
    } catch (err) {
      console.error("Failed to fetch books", err);
    } finally {
      setIsLoading(false);
    }
  };

  const deleteBook = async (filename) => {
    if (!confirm(`Are you sure you want to delete ${filename}?`)) return;
    
    try {
      const res = await fetch(`${API_BASE_URL}/books/${filename}`, {
        method: 'DELETE'
      });
      if (res.ok) {
        setBooks(prev => prev.filter(b => b !== filename));
      } else {
        alert('Failed to delete book');
      }
    } catch (err) {
      console.error("Failed to delete book", err);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm">
      <div className="bg-[#171717] border border-gray-700 rounded-2xl shadow-2xl w-full max-w-lg overflow-hidden flex flex-col max-h-[80vh]">
        <div className="flex items-center justify-between p-4 border-b border-gray-800">
          <h2 className="text-xl font-semibold text-white flex items-center gap-2">
            <BookIcon /> Manage Uploaded Books
          </h2>
          <button 
            onClick={onClose}
            className="p-1 hover:bg-[#2f2f2f] rounded-lg text-gray-400 hover:text-white transition-colors"
          >
            <CloseIcon />
          </button>
        </div>
        
        <div className="p-4 flex-1 overflow-y-auto custom-scrollbar">
          {isLoading ? (
            <div className="flex justify-center items-center py-8 text-purple-400">
              <LoaderIcon />
            </div>
          ) : books.length === 0 ? (
            <div className="text-center py-8 text-gray-400">
              No books uploaded yet.
            </div>
          ) : (
            <ul className="space-y-2">
              {books.map((book, idx) => (
                <li key={idx} className="flex items-center justify-between p-3 bg-[#212121] rounded-lg border border-gray-800 hover:border-gray-700 transition-colors">
                  <div className="flex items-center gap-3 overflow-hidden">
                    <BookIcon />
                    <span className="truncate text-sm text-gray-200">{book}</span>
                  </div>
                  <button 
                    onClick={() => deleteBook(book)}
                    className="text-gray-400 hover:text-red-400 p-2 hover:bg-[#2f2f2f] rounded-md transition-colors"
                    title="Delete book"
                  >
                    <TrashIcon />
                  </button>
                </li>
              ))}
            </ul>
          )}
        </div>
      </div>
    </div>
  );
}
