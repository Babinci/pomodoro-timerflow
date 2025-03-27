import React, { useState, useEffect } from 'react';

const MarkdownEditor = () => {
  const [markdown, setMarkdown] = useState('# Hello World\n\nStart typing your markdown here...');
  const [isEditing, setIsEditing] = useState(false);
  
  // Function to render markdown preview
  const renderMarkdown = (text) => {
    // Simple markdown rendering implementation
    return text
      .replace(/^# (.*$)/gm, '<h1>$1</h1>')
      .replace(/^## (.*$)/gm, '<h2>$1</h2>')
      .replace(/^### (.*$)/gm, '<h3>$1</h3>')
      .replace(/\*\*(.*)\*\*/gm, '<strong>$1</strong>')
      .replace(/\*(.*)\*/gm, '<em>$1</em>')
      .replace(/^\- (.*$)/gm, '<ul><li>$1</li></ul>')
      .replace(/\n/gm, '<br />');
  };

  // Insert formatting at cursor position or around selected text
  const insertFormatting = (type) => {
    // If not in edit mode, switch to edit mode first
    if (!isEditing) {
      setIsEditing(true);
      // Allow the textarea to render before trying to focus
      setTimeout(() => {
        const textarea = document.getElementById('markdown-textarea');
        textarea.focus();
        insertFormat(type, textarea);
      }, 100);
      return;
    }
    
    const textarea = document.getElementById('markdown-textarea');
    insertFormat(type, textarea);
  };
  
  const insertFormat = (type, textarea) => {
    const start = textarea.selectionStart;
    const end = textarea.selectionEnd;
    const selectedText = markdown.substring(start, end);
    
    let formattedText = '';
    let cursorOffset = 0;
    
    switch(type) {
      case 'h1':
        formattedText = `# ${selectedText}`;
        cursorOffset = 2;
        break;
      case 'h2':
        formattedText = `## ${selectedText}`;
        cursorOffset = 3;
        break;
      case 'h3':
        formattedText = `### ${selectedText}`;
        cursorOffset = 4;
        break;
      case 'bold':
        formattedText = `**${selectedText}**`;
        cursorOffset = 2;
        break;
      case 'italic':
        formattedText = `*${selectedText}*`;
        cursorOffset = 1;
        break;
      case 'list':
        formattedText = `- ${selectedText}`;
        cursorOffset = 2;
        break;
      case 'tab':
        formattedText = `    ${selectedText}`;
        cursorOffset = 4;
        break;
      default:
        formattedText = selectedText;
    }
    
    const newText = markdown.substring(0, start) + formattedText + markdown.substring(end);
    setMarkdown(newText);
    
    // Set cursor position after update
    setTimeout(() => {
      textarea.focus();
      const newPosition = selectedText ? start + formattedText.length : start + cursorOffset;
      textarea.setSelectionRange(newPosition, newPosition);
    }, 0);
  };

  const toggleEditMode = () => {
    setIsEditing(!isEditing);
    // Focus the textarea when switching to edit mode
    if (!isEditing) {
      setTimeout(() => {
        const textarea = document.getElementById('markdown-textarea');
        if (textarea) textarea.focus();
      }, 100);
    }
  };

  return (
    <div className="flex flex-col w-full max-w-2xl mx-auto bg-white rounded-lg shadow-lg overflow-hidden">
      {/* Toolbar */}
      <div className="bg-gray-100 p-3 border-b border-gray-300">
        <div className="flex flex-wrap items-center gap-2">
          <button
            onClick={toggleEditMode}
            className={`px-3 py-1 rounded ${isEditing ? 'bg-blue-500 text-white' : 'bg-white border border-gray-300'}`}
          >
            {isEditing ? 'Preview' : 'Edit'}
          </button>
          
          <div className="h-6 border-l border-gray-300 mx-1"></div>
          
          <button
            onClick={() => insertFormatting('h1')}
            className="bg-white px-3 py-1 rounded border border-gray-300 hover:bg-gray-50 font-bold text-lg"
            title="Heading 1"
          >
            H1
          </button>
          <button
            onClick={() => insertFormatting('h2')}
            className="bg-white px-3 py-1 rounded border border-gray-300 hover:bg-gray-50 font-bold"
            title="Heading 2"
          >
            H2
          </button>
          <button
            onClick={() => insertFormatting('h3')}
            className="bg-white px-3 py-1 rounded border border-gray-300 hover:bg-gray-50 font-semibold text-sm"
            title="Heading 3"
          >
            H3
          </button>
          <button
            onClick={() => insertFormatting('bold')}
            className="bg-white px-3 py-1 rounded border border-gray-300 hover:bg-gray-50 font-bold"
            title="Bold"
          >
            B
          </button>
          <button
            onClick={() => insertFormatting('italic')}
            className="bg-white px-3 py-1 rounded border border-gray-300 hover:bg-gray-50 italic"
            title="Italic"
          >
            I
          </button>
          <button
            onClick={() => insertFormatting('list')}
            className="bg-white px-3 py-1 rounded border border-gray-300 hover:bg-gray-50"
            title="Bulleted List"
          >
            • List
          </button>
          <button
            onClick={() => insertFormatting('tab')}
            className="bg-white px-3 py-1 rounded border border-gray-300 hover:bg-gray-50"
            title="Tab Indent"
          >
            ⇥ Tab
          </button>
        </div>
      </div>
      
      {/* Content Area - Conditionally show editor or preview */}
      <div className="p-4">
        {isEditing ? (
          <textarea
            id="markdown-textarea"
            className="w-full h-64 p-3 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500 font-mono"
            value={markdown}
            onChange={(e) => setMarkdown(e.target.value)}
            placeholder="Type your markdown here..."
          />
        ) : (
          <div 
            className="w-full min-h-64 p-3 border border-gray-300 rounded-lg prose prose-sm"
            dangerouslySetInnerHTML={{ __html: renderMarkdown(markdown) }}
            onClick={toggleEditMode}
          />
        )}
        
        {!isEditing && (
          <div className="mt-2 text-sm text-gray-500 italic">
            Click on the preview to edit, or use the formatting buttons to insert elements
          </div>
        )}
      </div>
    </div>
  );
};

export default MarkdownEditor;