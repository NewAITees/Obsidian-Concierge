document.addEventListener('DOMContentLoaded', () => {
  // Base API URL
  const API_BASE_URL = 'http://localhost:8000/api/v1';

  // Navigation handling
  function navigateTo(pageId) {
    // Hide all pages
    document.querySelectorAll('.page').forEach(page => {
      page.classList.add('hidden');
    });
    
    // Show selected page
    const targetPage = document.getElementById(`${pageId}-page`);
    if (targetPage) {
      targetPage.classList.remove('hidden');
    }
    
    // Update active navigation link
    document.querySelectorAll('.nav-item').forEach(link => {
      link.classList.remove('active');
    });
    
    document.querySelector(`.nav-item[data-page="${pageId}"]`)?.classList.add('active');
    
    // Update hash
    window.location.hash = pageId;
  }

  // Initialize based on URL hash
  function initializeFromHash() {
    const hash = window.location.hash.substring(1) || 'home';
    navigateTo(hash);
  }

  // Handle click on navigation links
  document.querySelectorAll('.nav-item').forEach(link => {
    link.addEventListener('click', (e) => {
      e.preventDefault();
      const pageId = link.getAttribute('data-page');
      navigateTo(pageId);
    });
  });

  // Check if the path exists and display an error if it doesn't
  window.addEventListener('hashchange', initializeFromHash);
  initializeFromHash();

  // API client functions
  const api = {
    async search(query, limit = 10, filters = null) {
      try {
        const response = await fetch(`${API_BASE_URL}/search`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            query,
            limit,
            filters,
          }),
        });
        
        if (!response.ok) {
          throw new Error(`API error: ${response.status}`);
        }
        
        return await response.json();
      } catch (error) {
        console.error('Search error:', error);
        throw error;
      }
    },
    
    async askQuestion(question, contextSize = 3, temperature = 0.7) {
      try {
        const response = await fetch(`${API_BASE_URL}/ask`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            question,
            context_size: contextSize,
            temperature,
          }),
        });
        
        if (!response.ok) {
          throw new Error(`API error: ${response.status}`);
        }
        
        return await response.json();
      } catch (error) {
        console.error('Question error:', error);
        throw error;
      }
    },
    
    async moveFile(source, destination = null, analyze = true) {
      try {
        const requestBody = {
          source,
          analyze,
        };
        
        if (!analyze && destination) {
          requestBody.destination = destination;
        }
        
        const response = await fetch(`${API_BASE_URL}/vault/move`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(requestBody),
        });
        
        if (!response.ok) {
          throw new Error(`API error: ${response.status}`);
        }
        
        return await response.json();
      } catch (error) {
        console.error('Move file error:', error);
        throw error;
      }
    },
    
    async generateMOC(type, params) {
      try {
        const requestBody = {
          type,
          file_path: params.filePath,
        };
        
        if (type === 'topic' && params.topic) {
          requestBody.topic = params.topic;
        } else if (type === 'folder' && params.folder) {
          requestBody.folder = params.folder;
        } else if (type === 'tag' && params.tag) {
          requestBody.tag = params.tag;
        }
        
        const response = await fetch(`${API_BASE_URL}/moc`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(requestBody),
        });
        
        if (!response.ok) {
          throw new Error(`API error: ${response.status}`);
        }
        
        return await response.json();
      } catch (error) {
        console.error('Generate MOC error:', error);
        throw error;
      }
    },
    
    async tagFile(path, tags = null, analyze = true) {
      try {
        const requestBody = {
          path,
          analyze,
        };
        
        if (!analyze && tags) {
          requestBody.tags = Array.isArray(tags) ? tags : tags.split(',').map(t => t.trim());
        }
        
        const response = await fetch(`${API_BASE_URL}/vault/tag`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(requestBody),
        });
        
        if (!response.ok) {
          throw new Error(`API error: ${response.status}`);
        }
        
        return await response.json();
      } catch (error) {
        console.error('Tag file error:', error);
        throw error;
      }
    },
    
    async healthCheck() {
      try {
        const response = await fetch(`${API_BASE_URL}/health`);
        return response.ok;
      } catch (error) {
        console.error('Health check error:', error);
        return false;
      }
    }
  };

  // Helper functions
  function showLoading(id) {
    document.getElementById(id).classList.remove('hidden');
  }
  
  function hideLoading(id) {
    document.getElementById(id).classList.add('hidden');
  }
  
  function showElement(id) {
    document.getElementById(id).classList.remove('hidden');
  }
  
  function hideElement(id) {
    document.getElementById(id).classList.add('hidden');
  }
  
  function createTag(text) {
    const tag = document.createElement('div');
    tag.className = 'tag';
    tag.textContent = text;
    
    const closeButton = document.createElement('span');
    closeButton.className = 'tag-close';
    closeButton.textContent = '×';
    closeButton.addEventListener('click', () => {
      tag.remove();
    });
    
    tag.appendChild(closeButton);
    return tag;
  }

  // Search functionality
  const searchButton = document.getElementById('search-button');
  const searchQuery = document.getElementById('search-query');
  const searchResults = document.getElementById('search-results');
  const searchTagsCheckbox = document.getElementById('search-tags');
  const tagsFilter = document.getElementById('tags-filter');
  const tagInput = document.getElementById('tag-input');
  const addTagButton = document.getElementById('add-tag-button');
  const selectedTags = document.getElementById('selected-tags');
  
  searchTagsCheckbox?.addEventListener('change', () => {
    if (searchTagsCheckbox.checked) {
      showElement('tags-filter');
    } else {
      hideElement('tags-filter');
    }
  });
  
  addTagButton?.addEventListener('click', () => {
    const tagValue = tagInput.value.trim();
    if (tagValue) {
      selectedTags.appendChild(createTag(tagValue));
      tagInput.value = '';
    }
  });
  
  searchButton?.addEventListener('click', async () => {
    const query = searchQuery.value.trim();
    if (!query) return;
    
    searchResults.innerHTML = '';
    showLoading('search-loading');
    
    try {
      // Collect tags if filter is enabled
      let filters = null;
      if (searchTagsCheckbox.checked) {
        const tags = Array.from(selectedTags.querySelectorAll('.tag'))
          .map(tag => tag.textContent.replace('×', '').trim());
        
        if (tags.length > 0) {
          filters = { tags };
        }
      }
      
      const result = await api.search(query, 10, filters);
      
      hideLoading('search-loading');
      
      if (result.results.length === 0) {
        searchResults.innerHTML = '<p class="text-center text-gray-500">検索結果がありません</p>';
        return;
      }
      
      result.results.forEach(item => {
        const resultElement = document.createElement('div');
        resultElement.className = 'search-result';
        
        resultElement.innerHTML = `
          <h3 class="search-result-title">${item.title}</h3>
          <p class="search-result-path">${item.path}</p>
          <p class="search-result-excerpt">${item.excerpt}</p>
          <div class="mt-2 text-right">
            <span class="text-sm text-gray-500">関連度: ${Math.round(item.relevance * 100)}%</span>
          </div>
        `;
        
        searchResults.appendChild(resultElement);
      });
    } catch (error) {
      hideLoading('search-loading');
      searchResults.innerHTML = `<p class="text-center text-red-500">エラーが発生しました: ${error.message}</p>`;
    }
  });

  // Question answering functionality
  const askButton = document.getElementById('ask-button');
  const questionInput = document.getElementById('question-input');
  const answerContainer = document.getElementById('answer-container');
  const answerContent = document.getElementById('answer-content');
  const answerSources = document.getElementById('answer-sources');
  const followupQuestions = document.getElementById('followup-questions');
  const advancedOptionsCheckbox = document.getElementById('advanced-options');
  const qaOptions = document.getElementById('qa-options');
  const contextSizeSlider = document.getElementById('context-size');
  const temperatureSlider = document.getElementById('temperature');
  
  advancedOptionsCheckbox?.addEventListener('change', () => {
    if (advancedOptionsCheckbox.checked) {
      showElement('qa-options');
    } else {
      hideElement('qa-options');
    }
  });
  
  askButton?.addEventListener('click', async () => {
    const question = questionInput.value.trim();
    if (!question) return;
    
    hideElement('answer-container');
    showLoading('qa-loading');
    
    try {
      // Get values from sliders
      const contextSize = parseInt(contextSizeSlider.value);
      const temperature = parseInt(temperatureSlider.value) / 10; // Convert 0-10 to 0-1.0
      
      const result = await api.askQuestion(question, contextSize, temperature);
      
      hideLoading('qa-loading');
      showElement('answer-container');
      
      // Display answer
      answerContent.innerHTML = result.answer.replace(/\n/g, '<br>');
      
      // Display sources
      answerSources.innerHTML = '';
      if (result.context && result.context.length > 0) {
        result.context.forEach(source => {
          const sourceElement = document.createElement('div');
          sourceElement.className = 'mb-2';
          sourceElement.innerHTML = `
            <p><strong>${source.title}</strong> (${source.path})</p>
          `;
          answerSources.appendChild(sourceElement);
        });
      } else {
        answerSources.innerHTML = '<p class="text-gray-500">ソースが見つかりませんでした</p>';
      }
      
      // Display follow-up questions
      followupQuestions.innerHTML = '';
      if (result.followup_questions && result.followup_questions.length > 0) {
        result.followup_questions.forEach(q => {
          const questionButton = document.createElement('button');
          questionButton.className = 'button button-secondary';
          questionButton.textContent = q;
          questionButton.addEventListener('click', () => {
            questionInput.value = q;
            askButton.click();
          });
          followupQuestions.appendChild(questionButton);
        });
      } else {
        // Generate dummy follow-up questions
        const dummyQuestions = [
          '詳細について教えてください',
          'この情報はどのように活用できますか？',
          '関連するトピックはありますか？'
        ];
        
        dummyQuestions.forEach(q => {
          const questionButton = document.createElement('button');
          questionButton.className = 'button button-secondary';
          questionButton.textContent = q;
          questionButton.addEventListener('click', () => {
            questionInput.value = q;
            askButton.click();
          });
          followupQuestions.appendChild(questionButton);
        });
      }
    } catch (error) {
      hideLoading('qa-loading');
      answerContainer.classList.remove('hidden');
      answerContent.innerHTML = `<p class="text-red-500">エラーが発生しました: ${error.message}</p>`;
      answerSources.innerHTML = '';
      followupQuestions.innerHTML = '';
    }
  });

  // File mover functionality
  const moveButton = document.getElementById('move-button');
  const filePath = document.getElementById('file-path');
  const analyzeMoveRadio = document.getElementById('analyze-move');
  const manualMoveRadio = document.getElementById('manual-move');
  const destinationContainer = document.getElementById('destination-container');
  const destinationPath = document.getElementById('destination-path');
  const moveResult = document.getElementById('move-result');
  const moveMessage = document.getElementById('move-message');
  const moveSource = document.getElementById('move-source');
  const moveDestination = document.getElementById('move-destination');
  
  manualMoveRadio?.addEventListener('change', () => {
    if (manualMoveRadio.checked) {
      showElement('destination-container');
    } else {
      hideElement('destination-container');
    }
  });
  
  analyzeMoveRadio?.addEventListener('change', () => {
    if (analyzeMoveRadio.checked) {
      hideElement('destination-container');
    } else {
      showElement('destination-container');
    }
  });
  
  moveButton?.addEventListener('click', async () => {
    const source = filePath.value.trim();
    if (!source) return;
    
    let destination = null;
    const analyze = analyzeMoveRadio.checked;
    
    if (!analyze) {
      destination = destinationPath.value.trim();
      if (!destination) return;
    }
    
    hideElement('move-result');
    showLoading('move-loading');
    
    try {
      const result = await api.moveFile(source, destination, analyze);
      
      hideLoading('move-loading');
      showElement('move-result');
      
      moveMessage.textContent = result.message;
      moveSource.textContent = result.source;
      moveDestination.textContent = result.destination;
    } catch (error) {
      hideLoading('move-loading');
      showElement('move-result');
      moveMessage.innerHTML = `<span class="text-red-500">エラーが発生しました: ${error.message}</span>`;
      moveSource.textContent = source;
      moveDestination.textContent = '移動失敗';
    }
  });

  // MOC generator functionality
  const generateMocButton = document.getElementById('generate-moc-button');
  const topicMocRadio = document.getElementById('topic-moc');
  const folderMocRadio = document.getElementById('folder-moc');
  const tagMocRadio = document.getElementById('tag-moc');
  const topicInputContainer = document.getElementById('topic-input-container');
  const folderInputContainer = document.getElementById('folder-input-container');
  const tagInputContainer = document.getElementById('tag-input-container');
  const topicInput = document.getElementById('topic-input');
  const folderInput = document.getElementById('folder-input');
  const tagNameInput = document.getElementById('tag-name-input');
  const mocPath = document.getElementById('moc-path');
  const mocResult = document.getElementById('moc-result');
  const mocMessage = document.getElementById('moc-message');
  const mocFilePath = document.getElementById('moc-file-path');
  const mocIncludedFiles = document.getElementById('moc-included-files');
  const viewMocButton = document.getElementById('view-moc-button');
  const mocPreviewModal = document.getElementById('moc-preview-modal');
  const closeMocModal = document.getElementById('close-moc-modal');
  const closePreviewButton = document.getElementById('close-preview-button');
  const mocPreviewContent = document.getElementById('moc-preview-content');
  
  // MOC type radio change handlers
  topicMocRadio?.addEventListener('change', () => {
    if (topicMocRadio.checked) {
      showElement('topic-input-container');
      hideElement('folder-input-container');
      hideElement('tag-input-container');
    }
  });
  
  folderMocRadio?.addEventListener('change', () => {
    if (folderMocRadio.checked) {
      hideElement('topic-input-container');
      showElement('folder-input-container');
      hideElement('tag-input-container');
    }
  });
  
  tagMocRadio?.addEventListener('change', () => {
    if (tagMocRadio.checked) {
      hideElement('topic-input-container');
      hideElement('folder-input-container');
      showElement('tag-input-container');
    }
  });
  
  // Generate MOC button click handler
  generateMocButton?.addEventListener('click', async () => {
    let type = 'topic';
    let params = { filePath: mocPath.value.trim() };
    
    if (topicMocRadio.checked) {
      type = 'topic';
      params.topic = topicInput.value.trim();
      if (!params.topic) return;
    } else if (folderMocRadio.checked) {
      type = 'folder';
      params.folder = folderInput.value.trim();
      if (!params.folder) return;
    } else if (tagMocRadio.checked) {
      type = 'tag';
      params.tag = tagNameInput.value.trim();
      if (!params.tag) return;
    }
    
    if (!params.filePath) return;
    
    hideElement('moc-result');
    showLoading('moc-loading');
    
    try {
      const result = await api.generateMOC(type, params);
      
      hideLoading('moc-loading');
      showElement('moc-result');
      
      mocMessage.textContent = 'MOC generated and saved successfully!';
      mocFilePath.textContent = result.file_path;
      mocIncludedFiles.textContent = result.included_files;
    } catch (error) {
      hideLoading('moc-loading');
      showElement('moc-result');
      mocMessage.innerHTML = `<span class="text-red-500">エラーが発生しました: ${error.message}</span>`;
      mocFilePath.textContent = params.filePath;
      mocIncludedFiles.textContent = '0';
    }
  });

  // Tag management functionality
  const tagButton = document.getElementById('tag-button');
  const tagFilePath = document.getElementById('tag-file-path');
  const analyzeTagsRadio = document.getElementById('analyze-tags');
  const manualTagsRadio = document.getElementById('manual-tags');
  const manualTagsContainer = document.getElementById('manual-tags-container');
  const tagsInput = document.getElementById('tags-input');
  const tagResult = document.getElementById('tag-result');
  const tagMessage = document.getElementById('tag-message');
  const taggedFilePath = document.getElementById('tagged-file-path');
  const appliedTags = document.getElementById('applied-tags');
  
  manualTagsRadio?.addEventListener('change', () => {
    if (manualTagsRadio.checked) {
      showElement('manual-tags-container');
    } else {
      hideElement('manual-tags-container');
    }
  });
  
  analyzeTagsRadio?.addEventListener('change', () => {
    if (analyzeTagsRadio.checked) {
      hideElement('manual-tags-container');
    } else {
      showElement('manual-tags-container');
    }
  });
  
  tagButton?.addEventListener('click', async () => {
    const path = tagFilePath.value.trim();
    if (!path) return;
    
    let tags = null;
    const analyze = analyzeTagsRadio.checked;
    
    if (!analyze) {
      const tagsValue = tagsInput.value.trim();
      if (!tagsValue) return;
      tags = tagsValue;
    }
    
    hideElement('tag-result');
    showLoading('tag-loading');
    
    try {
      const result = await api.tagFile(path, tags, analyze);
      
      hideLoading('tag-loading');
      showElement('tag-result');
      
      tagMessage.textContent = result.message;
      taggedFilePath.textContent = result.path;
      
      // Display applied tags
      appliedTags.innerHTML = '';
      if (result.tags && result.tags.length > 0) {
        result.tags.forEach(tag => {
          appliedTags.appendChild(createTag(tag));
        });
      } else {
        appliedTags.innerHTML = '<p class="text-gray-500">タグが適用されませんでした</p>';
      }
    } catch (error) {
      hideLoading('tag-loading');
      showElement('tag-result');
      tagMessage.innerHTML = `<span class="text-red-500">エラーが発生しました: ${error.message}</span>`;
      taggedFilePath.textContent = path;
      appliedTags.innerHTML = '';
    }
  });

  // Check API health on load
  (async () => {
    try {
      const healthy = await api.healthCheck();
      if (!healthy) {
        alert('APIサーバーに接続できません。サーバーが実行されていることを確認してください。');
      }
    } catch (error) {
      console.error('Health check failed:', error);
    }
  })();

  class Modal {
    constructor() {
      this.backdrop = document.querySelector('.modal-backdrop');
      this.content = this.backdrop?.querySelector('.modal-content');
      this.closeButton = this.backdrop?.querySelector('.modal-close');
      this.isOpen = false;
      this.previousActiveElement = null;
      this.focusableElements = null;
      this.firstFocusableElement = null;
      this.lastFocusableElement = null;

      this.handleKeyDown = this.handleKeyDown.bind(this);
      this.handleBackdropClick = this.handleBackdropClick.bind(this);
      this.init();
    }

    init() {
      if (!this.backdrop || !this.content) return;
      
      this.closeButton?.addEventListener('click', () => this.close());
      this.backdrop.addEventListener('click', this.handleBackdropClick);
      document.addEventListener('keydown', this.handleKeyDown);
    }

    open() {
      if (!this.backdrop || this.isOpen) return;
      
      this.isOpen = true;
      this.previousActiveElement = document.activeElement;
      this.backdrop.classList.add('show');
      document.body.style.overflow = 'hidden';
      
      // Update focusable elements
      this.focusableElements = this.content.querySelectorAll(
        'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
      );
      this.firstFocusableElement = this.focusableElements[0];
      this.lastFocusableElement = this.focusableElements[this.focusableElements.length - 1];
      
      // Focus the first focusable element
      requestAnimationFrame(() => {
        this.firstFocusableElement?.focus();
      });
    }

    close() {
      if (!this.backdrop || !this.isOpen) return;
      
      this.isOpen = false;
      this.backdrop.classList.remove('show');
      document.body.style.overflow = '';
      
      // Restore focus to the previous element
      requestAnimationFrame(() => {
        this.previousActiveElement?.focus();
      });
    }

    handleKeyDown(event) {
      if (!this.isOpen) return;

      if (event.key === 'Escape') {
        this.close();
        return;
      }

      if (event.key === 'Tab') {
        // Trap focus within the modal
        if (!event.shiftKey && document.activeElement === this.lastFocusableElement) {
          event.preventDefault();
          this.firstFocusableElement?.focus();
        } else if (event.shiftKey && document.activeElement === this.firstFocusableElement) {
          event.preventDefault();
          this.lastFocusableElement?.focus();
        }
      }
    }

    handleBackdropClick(event) {
      if (event.target === this.backdrop) {
        this.close();
      }
    }

    setContent(html) {
      if (this.content) {
        this.content.innerHTML = html;
      }
    }
  }

  // Initialize modal
  const modal = new Modal();

  // Update existing modal-related code to use the new Modal class
  function showMocPreview(mocHtml) {
    modal.setContent(`
      <div class="modal-header">
        <h2 class="modal-title">MOC Preview</h2>
        <button class="modal-close" aria-label="Close modal">×</button>
      </div>
      <div class="modal-body">
        ${mocHtml}
      </div>
    `);
    modal.open();
  }
}); 