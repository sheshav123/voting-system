// Unified Voter Portal JavaScript with Firebase OTP and Voting Integration

// Firebase Configuration for Google Sign-In
const firebaseConfig = {
    apiKey: "AIzaSyDZbf7pE7f6c2_WwmpPjwV21RGiwkvKI1M",
    authDomain: "voting-system-2024.firebaseapp.com",
    projectId: "voting-system-2024",
    storageBucket: "voting-system-2024.firebasestorage.app",
    messagingSenderId: "321203170985",
    appId: "1:321203170985:web:2e971e12017170b8fc43b8"
};

// Initialize Firebase
firebase.initializeApp(firebaseConfig);

// Global variables
let confirmationResult = null;
let selectedCandidateId = null;
let currentVoter = null;

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    setupEventListeners();
    checkExistingSession();
});

function setupEventListeners() {
    // Photo file input
    const photoFileInput = document.getElementById('photo-file');
    if (photoFileInput) {
        photoFileInput.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    document.getElementById('preview-image').src = e.target.result;
                    document.getElementById('photo-preview').classList.remove('d-none');
                };
                reader.readAsDataURL(file);
            }
        });
    }
}

// Check for existing session on page load
async function checkExistingSession() {
    try {
        console.log('🔍 Checking for existing session...');
        
        // Check if user has an active session with the backend
        const response = await fetch('/voter-info', {
            method: 'GET',
            credentials: 'same-origin'
        });
        
        const result = await response.json();
        
        if (result.success && result.voter) {
            console.log('✅ Found existing session for:', result.voter.name);
            currentVoter = result.voter;
            showVoterDashboard();
            return;
        }
        
        console.log('ℹ️ No existing session found, showing login');
        
        // Initialize Firebase auth state listener
        firebase.auth().onAuthStateChanged(function(user) {
            if (user && !currentVoter) {
                console.log('🔥 Firebase user detected, verifying with backend...');
                verifyFirebaseUser(user);
            }
        });
        
    } catch (error) {
        console.error('❌ Error checking session:', error);
        // Show login form if session check fails
        document.getElementById('login-section').classList.remove('d-none');
        document.getElementById('voter-dashboard').classList.add('d-none');
    }
}

// Verify Firebase user with backend
async function verifyFirebaseUser(user) {
    try {
        const idToken = await user.getIdToken();
        
        const verifyResult = await apiCall('/verify-google-token', {
            method: 'POST',
            body: JSON.stringify({ idToken: idToken })
        });
        
        if (verifyResult.success) {
            currentVoter = verifyResult.voter;
            console.log('✅ Session restored for:', currentVoter.name);
            showVoterDashboard();
        } else {
            console.log('❌ Backend verification failed:', verifyResult.message);
            // Sign out from Firebase if backend verification fails
            firebase.auth().signOut();
        }
    } catch (error) {
        console.error('❌ Error verifying Firebase user:', error);
        firebase.auth().signOut();
    }
}

// Utility functions
function showAlert(message, type = 'info') {
    const alertContainer = document.getElementById('alert-container');
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show mt-3`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    alertContainer.appendChild(alertDiv);
    
    setTimeout(() => {
        if (alertDiv.parentNode) {
            alertDiv.remove();
        }
    }, 5000);
}

function showLoading(show = true) {
    const loading = document.getElementById('loading');
    const steps = document.querySelectorAll('.step:not(#loading)');
    
    if (show) {
        steps.forEach(step => step.classList.add('d-none'));
        loading.classList.remove('d-none');
    } else {
        loading.classList.add('d-none');
    }
}

// Google Sign-In uses single step - no step switching needed

// API call wrapper
async function apiCall(url, options = {}) {
    try {
        const response = await fetch(url, {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        });
        
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('API Error:', error);
        return { success: false, message: 'Network error occurred' };
    }
}

// Firebase OTP Functions
// Google Sign-In Functions
async function signInWithGoogle() {
    try {
        showLoading(true);
        
        console.log('🔐 Initiating Google Sign-In...');
        
        // Configure Google Auth Provider
        const provider = new firebase.auth.GoogleAuthProvider();
        provider.addScope('email');
        provider.addScope('profile');
        
        // Sign in with popup
        const result = await firebase.auth().signInWithPopup(provider);
        const user = result.user;
        
        console.log('✅ Google Sign-In successful:', user.email);
        
        // Get ID token
        const idToken = await user.getIdToken();
        
        // Verify with backend
        const verifyResult = await apiCall('/verify-google-token', {
            method: 'POST',
            body: JSON.stringify({ idToken: idToken })
        });
        
        showLoading(false);
        
        if (verifyResult.success) {
            currentVoter = verifyResult.voter;
            showAlert('✅ Welcome! Google authentication successful.', 'success');
            showVoterDashboard();
        } else {
            showAlert('❌ ' + verifyResult.message, 'danger');
            // Sign out from Firebase if backend verification fails
            firebase.auth().signOut();
        }
        
    } catch (error) {
        showLoading(false);
        console.error('❌ Google Sign-In Error:', error);
        
        let errorMessage = 'Google Sign-In failed: ';
        
        switch (error.code) {
            case 'auth/popup-closed-by-user':
                errorMessage += 'Sign-in was cancelled. Please try again.';
                break;
            case 'auth/popup-blocked':
                errorMessage += 'Popup was blocked. Please allow popups and try again.';
                break;
            case 'auth/network-request-failed':
                errorMessage += 'Network error. Please check your internet connection.';
                break;
            case 'auth/too-many-requests':
                errorMessage += 'Too many attempts. Please try again later.';
                break;
            default:
                errorMessage += error.message || 'Unknown error occurred.';
        }
        
        showAlert(errorMessage, 'danger');
    }
}

// Google Sign-In is handled in signInWithGoogle() function above

// Dashboard Functions
function showVoterDashboard() {
    document.getElementById('login-section').classList.add('d-none');
    document.getElementById('voter-dashboard').classList.remove('d-none');
    
    // Populate voter details
    document.getElementById('voter-name').textContent = currentVoter.name;
    document.getElementById('voter-roll').textContent = currentVoter.roll_number;
    document.getElementById('voter-phone').textContent = currentVoter.phone;
    document.getElementById('voter-email').textContent = currentVoter.email;
    
    // Show voter photo if available
    if (currentVoter.photo) {
        const photoContainer = document.getElementById('voter-photo-container');
        photoContainer.innerHTML = `
            <img src="/static/uploads/${currentVoter.photo}" alt="${currentVoter.name}" class="voter-photo">
        `;
    }
    
    // Load election status
    loadElectionStatus();
}

async function loadElectionStatus() {
    try {
        const result = await apiCall('/election-status');
        const statusBanner = document.getElementById('election-status-banner');
        const voteBtn = document.getElementById('vote-now-btn');
        const resultsBtn = document.getElementById('view-results-btn');
        
        if (result.success && result.election) {
            const election = result.election;
            
            // Check if voter has voted
            const voterStatus = await apiCall('/check-voter-status', {
                method: 'POST',
                body: JSON.stringify({ phone: currentVoter.phone })
            });
            
            if (voterStatus.has_voted) {
                // Voter has already voted
                statusBanner.className = 'status-card status-voted';
                statusBanner.innerHTML = `
                    <div class="text-center">
                        <i class="fas fa-check-circle fa-3x mb-3"></i>
                        <h4>✅ Vote Recorded Successfully!</h4>
                        <p class="mb-0">Thank you for participating in: <strong>${election.title}</strong></p>
                        <small class="text-white-50">
                            <i class="fas fa-info-circle"></i> 
                            Your vote is secure and anonymous. Results will be available when the election ends.
                        </small>
                    </div>
                `;
                voteBtn.classList.add('d-none');
                resultsBtn.classList.remove('d-none');
                
                // Hide voting section if it's open
                document.getElementById('voting-section').classList.add('d-none');
            } else {
                // Voter can vote
                statusBanner.className = 'status-card status-active';
                statusBanner.innerHTML = `
                    <div class="text-center">
                        <i class="fas fa-vote-yea fa-3x mb-3"></i>
                        <h4>🗳️ Ready to Vote!</h4>
                        <p class="mb-0">Election: <strong>${election.title}</strong></p>
                        <small class="text-white-50">${election.description}</small>
                        <div class="mt-3">
                            <button class="btn btn-light btn-lg" onclick="startVoting()">
                                <i class="fas fa-vote-yea"></i> Vote Now
                            </button>
                        </div>
                    </div>
                `;
                voteBtn.classList.add('d-none'); // Hide separate vote button since it's in the banner
                resultsBtn.classList.add('d-none');
            }
            
            // Update election info
            document.getElementById('election-info').innerHTML = `
                <h6><i class="fas fa-vote-yea"></i> ${election.title}</h6>
                <p class="mb-2">${election.description}</p>
                <div class="row">
                    <div class="col-md-6">
                        <small class="text-muted">
                            <i class="fas fa-calendar"></i> Started: ${new Date(election.started_at).toLocaleString()}
                        </small>
                    </div>
                    <div class="col-md-6">
                        <small class="text-success">
                            <i class="fas fa-circle"></i> Status: Active
                        </small>
                    </div>
                </div>
            `;
            
        } else {
            // No active election - check for last election results
            const lastElection = await apiCall('/get-last-election');
            
            if (lastElection.success && lastElection.election) {
                statusBanner.className = 'status-card status-ended';
                statusBanner.innerHTML = `
                    <div class="text-center">
                        <i class="fas fa-flag-checkered fa-3x mb-3"></i>
                        <h4>Election Ended</h4>
                        <p class="mb-0">Last Election: <strong>${lastElection.election.title}</strong></p>
                        <small>View detailed results below</small>
                    </div>
                `;
                voteBtn.classList.add('d-none');
                resultsBtn.classList.remove('d-none');
                
                document.getElementById('election-info').innerHTML = `
                    <div class="alert alert-info">
                        <i class="fas fa-info-circle"></i> No active election. Last election: <strong>${lastElection.election.title}</strong> ended on ${new Date(lastElection.election.ended_at).toLocaleString()}
                    </div>
                `;
            } else {
                statusBanner.className = 'status-card status-inactive';
                statusBanner.innerHTML = `
                    <div class="text-center">
                        <i class="fas fa-clock fa-3x mb-3"></i>
                        <h4>No Active Election</h4>
                        <p class="mb-0">Please check back later</p>
                    </div>
                `;
                voteBtn.classList.add('d-none');
                resultsBtn.classList.add('d-none');
                
                document.getElementById('election-info').innerHTML = `
                    <div class="alert alert-info">
                        <i class="fas fa-info-circle"></i> No active election at the moment. Check back later.
                    </div>
                `;
            }
        }
        
    } catch (error) {
        console.error('Error loading election status:', error);
        document.getElementById('election-status-banner').innerHTML = `
            <div class="alert alert-danger">
                <i class="fas fa-exclamation-triangle"></i> Error loading election status
            </div>
        `;
    }
}

// Integrated Voting Functions
async function startVoting() {
    try {
        // Check if user has already voted
        const statusResult = await apiCall('/check-voter-status', {
            method: 'POST',
            body: JSON.stringify({ phone: currentVoter.phone })
        });
        
        if (statusResult.has_voted) {
            showAlert('You have already voted in this election.', 'warning');
            return;
        }
        
        const result = await apiCall('/get-candidates');
        
        if (result.success) {
            displayCandidates(result.candidates);
            document.getElementById('voting-section').classList.remove('d-none');
            document.getElementById('voting-section').scrollIntoView({ behavior: 'smooth' });
            
            // Hide other sections to focus on voting
            document.getElementById('vote-now-btn').style.display = 'none';
        } else {
            showAlert(result.message, 'danger');
        }
    } catch (error) {
        showAlert('Error loading candidates', 'danger');
    }
}

function cancelVoting() {
    document.getElementById('voting-section').classList.add('d-none');
    document.getElementById('vote-now-btn').style.display = 'block';
    selectedCandidateId = null;
}

function displayCandidates(candidates) {
    const container = document.getElementById('candidates-container');
    
    if (candidates.length === 0) {
        container.innerHTML = `
            <div class="alert alert-warning text-center">
                <i class="fas fa-exclamation-triangle"></i> No candidates available for this election
            </div>
        `;
        return;
    }
    
    container.innerHTML = candidates.map(candidate => `
        <div class="candidate-card" onclick="selectCandidate('${candidate.id}', '${candidate.name}')">
            <div class="row align-items-center">
                <div class="col-auto">
                    ${candidate.photo ? 
                        `<img src="${candidate.photo}" alt="${candidate.name}" class="candidate-photo">` :
                        `<div class="candidate-photo d-flex align-items-center justify-content-center bg-light">
                            <i class="fas fa-user fa-2x text-muted"></i>
                        </div>`
                    }
                </div>
                <div class="col">
                    <h5 class="mb-1">${candidate.name}</h5>
                    <p class="text-muted mb-0">Candidate ID: ${candidate.id}</p>
                </div>
                <div class="col-auto">
                    <div class="form-check">
                        <input class="form-check-input" type="radio" name="candidate" id="radio-${candidate.id}" value="${candidate.id}">
                        <label class="form-check-label" for="radio-${candidate.id}">
                            <i class="fas fa-vote-yea fa-2x text-primary"></i>
                        </label>
                    </div>
                </div>
            </div>
        </div>
    `).join('');
    
    // Show voting actions
    document.getElementById('voting-actions').classList.remove('d-none');
}

function selectCandidate(candidateId, candidateName) {
    // Remove previous selection
    document.querySelectorAll('.candidate-card').forEach(card => {
        card.classList.remove('selected');
    });
    
    // Clear all radio buttons
    document.querySelectorAll('input[name="candidate"]').forEach(radio => {
        radio.checked = false;
    });
    
    // Select new candidate
    event.currentTarget.classList.add('selected');
    document.getElementById(`radio-${candidateId}`).checked = true;
    
    selectedCandidateId = candidateId;
    
    // Enable vote button
    const voteButton = document.getElementById('vote-button');
    voteButton.disabled = false;
    voteButton.innerHTML = `<i class="fas fa-vote-yea"></i> Vote for ${candidateName}`;
}

function proceedToVote() {
    if (!selectedCandidateId) {
        showAlert('Please select a candidate first', 'warning');
        return;
    }
    
    // Get candidate name
    const selectedRadio = document.querySelector('input[name="candidate"]:checked');
    const candidateCard = selectedRadio.closest('.candidate-card');
    const candidateName = candidateCard.querySelector('h5').textContent;
    
    document.getElementById('selected-candidate-name').textContent = candidateName;
    
    // Show confirmation modal
    const modal = new bootstrap.Modal(document.getElementById('confirmVoteModal'));
    modal.show();
}

async function confirmVote() {
    if (!selectedCandidateId) {
        showAlert('Please select a candidate', 'warning');
        return;
    }
    
    try {
        showLoading(true);
        
        const result = await apiCall('/cast-vote', {
            method: 'POST',
            body: JSON.stringify({ 
                candidate_id: selectedCandidateId,
                phone: currentVoter.phone
            })
        });
        
        showLoading(false);
        
        if (result.success) {
            showAlert('🎉 Vote cast successfully! Thank you for participating.', 'success');
            
            // Hide modal
            const modal = bootstrap.Modal.getInstance(document.getElementById('confirmVoteModal'));
            modal.hide();
            
            // Hide voting section
            document.getElementById('voting-section').classList.add('d-none');
            
            // Reset selection
            selectedCandidateId = null;
            
            // Refresh election status to show "voted" state
            loadElectionStatus();
            
            // Show celebration message
            setTimeout(() => {
                showAlert('Your vote has been recorded. You can now view results when the election ends.', 'info');
            }, 2000);
            
        } else {
            showAlert(result.message, 'danger');
        }
    } catch (error) {
        showLoading(false);
        showAlert('Error casting vote: ' + error.message, 'danger');
    }
}

// Results Functions
async function viewResults() {
    try {
        const result = await apiCall('/get-election-results');
        
        if (result.success) {
            displayResults(result.results);
            document.getElementById('results-section').classList.remove('d-none');
            document.getElementById('results-section').scrollIntoView({ behavior: 'smooth' });
        } else {
            showAlert(result.message, 'danger');
        }
    } catch (error) {
        showAlert('Error loading results', 'danger');
    }
}

function displayResults(results) {
    const container = document.getElementById('results-container');
    
    if (!results || !results.candidates || results.candidates.length === 0) {
        container.innerHTML = `
            <div class="alert alert-warning text-center">
                <i class="fas fa-exclamation-triangle"></i> No results available
            </div>
        `;
        return;
    }
    
    const totalVotes = results.total_votes;
    const winner = results.candidates[0];
    
    container.innerHTML = `
        <div class="row mb-4">
            <div class="col-md-6">
                <div class="card bg-primary text-white">
                    <div class="card-body text-center">
                        <h3>${totalVotes}</h3>
                        <p class="mb-0">Total Votes Cast</p>
                    </div>
                </div>
            </div>
            <div class="col-md-6">
                <div class="card bg-success text-white">
                    <div class="card-body text-center">
                        <h5>${winner.name}</h5>
                        <p class="mb-0">Winner (${winner.votes} votes)</p>
                    </div>
                </div>
            </div>
        </div>
        
        <h6 class="mb-3">Detailed Results:</h6>
        
        ${results.candidates.map((candidate, index) => {
            const percentage = totalVotes > 0 ? ((candidate.votes / totalVotes) * 100).toFixed(1) : 0;
            const isWinner = index === 0;
            
            return `
                <div class="results-card ${isWinner ? 'winner-card' : ''}">
                    <div class="row align-items-center">
                        <div class="col-auto">
                            ${candidate.photo ? 
                                `<img src="${candidate.photo}" alt="${candidate.name}" class="candidate-photo">` :
                                `<div class="candidate-photo d-flex align-items-center justify-content-center bg-light">
                                    <i class="fas fa-user fa-2x text-muted"></i>
                                </div>`
                            }
                        </div>
                        <div class="col">
                            <div class="d-flex justify-content-between align-items-center mb-2">
                                <h6 class="mb-0">
                                    ${candidate.name}
                                    ${isWinner ? '<i class="fas fa-crown text-warning ms-2"></i>' : ''}
                                </h6>
                                <span class="badge bg-primary">${candidate.votes} votes (${percentage}%)</span>
                            </div>
                            <div class="progress" style="height: 8px;">
                                <div class="progress-bar ${isWinner ? 'bg-success' : 'bg-info'}" 
                                     style="width: ${percentage}%"></div>
                            </div>
                        </div>
                    </div>
                </div>
            `;
        }).join('')}
        
        ${results.election ? `
            <div class="mt-4 p-3 bg-light rounded">
                <h6><i class="fas fa-info-circle"></i> Election Details</h6>
                <p class="mb-1"><strong>Title:</strong> ${results.election.title}</p>
                <p class="mb-1"><strong>Description:</strong> ${results.election.description}</p>
                <p class="mb-0"><strong>Period:</strong> ${new Date(results.election.started_at).toLocaleString()} - ${results.election.ended_at ? new Date(results.election.ended_at).toLocaleString() : 'Ongoing'}</p>
            </div>
        ` : ''}
    `;
}

// Photo upload functions
function showPhotoUpload() {
    const modal = new bootstrap.Modal(document.getElementById('photoUploadModal'));
    modal.show();
}

async function uploadPhoto() {
    const fileInput = document.getElementById('photo-file');
    const file = fileInput.files[0];
    
    if (!file) {
        showAlert('Please select a photo', 'warning');
        return;
    }
    
    if (!file.type.startsWith('image/')) {
        showAlert('Please select a valid image file', 'warning');
        return;
    }
    
    if (file.size > 5 * 1024 * 1024) { // 5MB limit
        showAlert('Photo size must be less than 5MB', 'warning');
        return;
    }
    
    const formData = new FormData();
    formData.append('photo', file);
    formData.append('phone', currentVoter.phone);
    
    try {
        const response = await fetch('/upload-voter-photo', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        
        if (result.success) {
            showAlert('Photo uploaded successfully!', 'success');
            
            // Update photo display
            const photoContainer = document.getElementById('voter-photo-container');
            photoContainer.innerHTML = `
                <img src="/static/uploads/${result.filename}" alt="Voter Photo" class="voter-photo">
            `;
            
            // Hide modal
            const modal = bootstrap.Modal.getInstance(document.getElementById('photoUploadModal'));
            modal.hide();
            
            // Clear file input
            fileInput.value = '';
            document.getElementById('photo-preview').classList.add('d-none');
        } else {
            showAlert(result.message, 'danger');
        }
    } catch (error) {
        showAlert('Error uploading photo: ' + error.message, 'danger');
    }
}

// Utility functions
function refreshStatus() {
    loadElectionStatus();
    showAlert('Status refreshed', 'info');
}

// Google Sign-In doesn't need rate limit suggestions

async function logout() {
    if (confirm('Are you sure you want to logout?')) {
        try {
            // Clear backend session first
            await apiCall('/logout', { method: 'POST' });
            
            // Sign out from Google/Firebase
            await firebase.auth().signOut();
            
            console.log('✅ User signed out successfully');
            currentVoter = null;
            
            // Clear any cached data
            sessionStorage.clear();
            localStorage.removeItem('voterSession');
            
            // Reload page to show login form
            window.location.reload();
        } catch (error) {
            console.error('❌ Sign out error:', error);
            // Force reload even if logout fails
            window.location.reload();
        }
    }
}