document.addEventListener('DOMContentLoaded', () => {
    const message = document.querySelector('#message');
    if (message) {
        setTimeout(() => {
            message.style.opacity = '0'; // Fade out the message
            setTimeout(() => {
                message.style.display = 'none'; // Remove it from the layout
            }, 500); // Match the CSS transition duration (0.5s = 500ms)
        }, 3000); // Wait for 3 seconds before fading out
    }
});

// const uploadArea = document.getElementById('upload-area');
// const previewArea = document.getElementById('preview-area');
// const fileInput = document.getElementById('file-input');

// // Add dragover event
// uploadArea.addEventListener('dragover', (e) => {
//     e.preventDefault();
//     e.stopPropagation();
//     uploadArea.classList.add('drag-active');
// });

// // Add dragleave event
// uploadArea.addEventListener('dragleave', (e) => {
//     e.preventDefault();
//     e.stopPropagation();
//     uploadArea.classList.remove('drag-active');
// });

// // Add drop event
// uploadArea.addEventListener('drop', (e) => {
//     e.preventDefault();
//     e.stopPropagation();
//     uploadArea.classList.remove('drag-active');

//     const files = e.dataTransfer?.files;
//     if (files && files.length > 0) {
//         handleFiles(files);
//     }
// });

// // Add change event for file input
// fileInput.addEventListener('change', (e) => {
//     const files = e.target.files;
//     if (files && files.length > 0) {
//         handleFiles(files);
//     }
// });

// // Handle files
// function handleFiles(files) {
//     Array.from(files).forEach((file) => {
//         if (file.type.startsWith('image/') || file.type.startsWith('image/')) {
//             const reader = new FileReader();
//             reader.onload = (e) => {
//                 const preview = document.createElement('div');
//                 preview.className = 'relative';

//                 if (file.type.startsWith('image/')) {
//                     preview.innerHTML = `
//                         <img src="${e.target.result}" class="w-full h-32 object-cover rounded-lg">
//                         <button onclick="this.parentElement.remove()" class="absolute top-1 right-1 bg-red-500 text-white rounded-full p-1">
//                             <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
//                                 <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
//                             </svg>
//                         </button>
//                     `;
//                 } else {
//                     preview.innerHTML = `
//                         <video src="${e.target.result}" class="w-full h-32 object-cover rounded-lg" controls></video>
//                         <button onclick="this.parentElement.remove()" class="absolute top-1 right-1 bg-red-500 text-white rounded-full p-1">
//                             <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
//                                 <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
//                             </svg>
//                         </button>
//                     `;
//                 }

//                 previewArea.appendChild(preview);
//             };

//             reader.readAsDataURL(file);
//         } else {
//             alert('Only image and video files are supported.');
//         }
//     });
// }
