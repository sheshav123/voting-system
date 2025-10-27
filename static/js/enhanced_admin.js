// Enhanced Admin Panel JavaScript

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    // Handle Enter key for admin login
    const secretKeyInput = document.getElementById('secret-key');
    if (secretKeyInput) {
        secretKeyInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                adminLogin();
            }
        });
    }
    
    // Check for existing admin session
    checkAdminSession();
});

// Check for existing admin session
async function checkAdminSession() {
    try {
        console.log('🔍 Checking for existing admin session...');
        
        // Try to access admin data to check if session exists
        const result = await apiCall('/admin/elections');
        
        if (result.success) {
            console.log('✅ Found existing admin session');
            // Hide login form and show dashboard
            document.getElementById('admin-login').classList.add('d-none');
            document.getElementById('admin-dashboard').classList.remove('d-none');
            
            // Load initial data
            loadElectionStatus();
            refreshResults();
            loadCandidates();
            loadElections();
            loadVoters();
            loadPastElectionsSummary();
        } else {
            console.log('ℹ️ No existing admin session found');
            // Show login form
            document.getElementById('admin-login').classList.remove('d-none');
            document.getElementById('admin-dashboard').classList.add('d-none');
        }
    } catch (error) {
        console.error('❌ Error checking admin session:', error);
        // Show login form if session check fails
        document.getElementById('admin-login').classList.remove('d-none');
        document.getElementById('admin-dashboard').classList.add('d-none');
    }
}

// Utility functions
function showAlert(message, type = 'info', containerId = 'admin-alert-container') {
    const alertContainer = document.getElementById(containerId);
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
        
        return await response.json();
    } catch (error) {
        console.error('API Error:', error);
        return { success: false, message: 'Network error occurred' };
    }
}

// Admin login
async function adminLogin() {
    const secretKeyInput = document.getElementById('secret-key');
    const secretKey = secretKeyInput.value.trim();
    
    if (!secretKey) {
        showAlert('Please enter the admin password', 'warning');
        return;
    }
    
    const result = await apiCall('/admin/login', {
        method: 'POST',
        body: JSON.stringify({ secret_key: secretKey })
    });
    
    if (result.success) {
        showAlert('Admin authenticated successfully!', 'success');
        document.getElementById('admin-login').classList.add('d-none');
        document.getElementById('admin-dashboard').classList.remove('d-none');
        
        // Load initial data
        loadElectionStatus();
        refreshResults();
        loadCandidates();
        loadElections();
        loadVoters();
        loadPastElectionsSummary();
    } else {
        showAlert(result.message, 'danger');
    }
}

// Load election status
async function loadElectionStatus() {
    try {
        const result = await apiCall('/admin/elections');
        
        if (result.success) {
            const currentElection = result.current_election;
            const statusDiv = document.getElementById('election-status');
            const titleEl = document.getElementById('election-title');
            const descEl = document.getElementById('election-description');
            const startBtn = document.getElementById('start-election-btn');
            const stopBtn = document.getElementById('stop-election-btn');
            
            if (currentElection && currentElection.status === 'active') {
                statusDiv.className = 'election-status status-active';
                titleEl.textContent = `Active: ${currentElection.title}`;
                descEl.textContent = currentElection.description;
                startBtn.classList.add('d-none');
                stopBtn.classList.remove('d-none');
            } else {
                statusDiv.className = 'election-status status-inactive';
                titleEl.textContent = 'No Active Election';
                descEl.textContent = 'Create or start an election to begin voting';
                startBtn.classList.remove('d-none');
                stopBtn.classList.add('d-none');
            }
        }
    } catch (error) {
        console.error('Error loading election status:', error);
    }
}

// Show start election modal
async function showStartElectionModal() {
    const result = await apiCall('/admin/elections');
    
    if (result.success) {
        const select = document.getElementById('election-select');
        select.innerHTML = '<option value="">Select an election...</option>';
        
        result.elections.forEach(election => {
            if (election.status !== 'active') {
                select.innerHTML += `<option value="${election.id}">${election.title}</option>`;
            }
        });
        
        const modal = new bootstrap.Modal(document.getElementById('startElectionModal'));
        modal.show();
    }
}

// Start election
async function startElection() {
    const select = document.getElementById('election-select');
    const electionId = select.value;
    
    if (!electionId) {
        showAlert('Please select an election', 'warning');
        return;
    }
    
    const result = await apiCall('/admin/start-election', {
        method: 'POST',
        body: JSON.stringify({ election_id: electionId })
    });
    
    if (result.success) {
        showAlert('Election started successfully!', 'success');
        const modal = bootstrap.Modal.getInstance(document.getElementById('startElectionModal'));
        modal.hide();
        loadElectionStatus();
        refreshResults();
    } else {
        showAlert(result.message, 'danger');
    }
}

// Stop election
async function stopElection() {
    if (!confirm('Are you sure you want to stop the current election? This action cannot be undone.')) {
        return;
    }
    
    const result = await apiCall('/admin/stop-election', {
        method: 'POST'
    });
    
    if (result.success) {
        showAlert('Election stopped successfully!', 'success');
        loadElectionStatus();
        refreshResults();
    } else {
        showAlert(result.message, 'danger');
    }
}

// Create election
async function createElection() {
    const titleInput = document.getElementById('election-title-input');
    const descInput = document.getElementById('election-description-input');
    
    const title = titleInput.value.trim();
    const description = descInput.value.trim();
    
    if (!title) {
        showAlert('Please enter election title', 'warning');
        return;
    }
    
    const result = await apiCall('/admin/create-election', {
        method: 'POST',
        body: JSON.stringify({ 
            title: title, 
            description: description 
        })
    });
    
    if (result.success) {
        showAlert('Election created successfully!', 'success');
        titleInput.value = '';
        descInput.value = '';
        loadElections();
    } else {
        showAlert(result.message, 'danger');
    }
}

// Load elections
async function loadElections() {
    const result = await apiCall('/admin/elections');
    
    if (result.success) {
        const container = document.getElementById('elections-list');
        
        if (result.elections.length === 0) {
            container.innerHTML = '<p class="text-muted">No elections created yet.</p>';
            return;
        }
        
        let html = '';
        result.elections.forEach(election => {
            const statusBadge = election.status === 'active' ? 
                '<span class="badge bg-success">Active</span>' :
                election.status === 'ended' ? 
                '<span class="badge bg-secondary">Ended</span>' :
                '<span class="badge bg-warning">Created</span>';
            
            const createdDate = new Date(election.created_at).toLocaleDateString();
            const endedDate = election.ended_at ? new Date(election.ended_at).toLocaleDateString() : null;
            
            html += `
                <div class="border rounded p-3 mb-2">
                    <div class="d-flex justify-content-between align-items-start">
                        <div class="flex-grow-1">
                            <h6>${election.title} ${statusBadge}</h6>
                            <p class="text-muted mb-1">${election.description}</p>
                            <small class="text-muted">
                                Created: ${createdDate}
                                ${endedDate ? `<br>Ended: ${endedDate}` : ''}
                                ${election.total_votes !== undefined ? `<br>Total Votes: ${election.total_votes}` : ''}
                            </small>
                        </div>
                        <div class="btn-group btn-group-sm">
                            ${election.status === 'ended' ? 
                                `<button class="btn btn-outline-info" onclick="viewElectionResults('${election.id}')" title="View Results">
                                    <i class="fas fa-chart-bar"></i>
                                </button>` : ''
                            }
                            ${election.status !== 'active' ? 
                                `<button class="btn btn-outline-danger" onclick="deleteElection('${election.id}', '${election.title}')" title="Delete">
                                    <i class="fas fa-trash"></i>
                                </button>` : ''
                            }
                        </div>
                    </div>
                </div>
            `;
        });
        
        container.innerHTML = html;
    }
}

// Delete election
async function deleteElection(electionId, electionTitle) {
    // Show confirmation modal
    showDeleteElectionModal(electionId, electionTitle);
}

// Show delete election confirmation modal
function showDeleteElectionModal(electionId, electionTitle) {
    const modalHtml = `
        <div class="modal fade" id="deleteElectionModal" tabindex="-1">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header bg-danger text-white">
                        <h5 class="modal-title">
                            <i class="fas fa-exclamation-triangle"></i> Delete Election
                        </h5>
                        <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <div class="alert alert-warning">
                            <i class="fas fa-warning"></i>
                            <strong>Warning:</strong> This action cannot be undone!
                        </div>
                        <p>You are about to delete the election:</p>
                        <div class="card">
                            <div class="card-body">
                                <h6 class="card-title">${electionTitle}</h6>
                                <p class="card-text text-muted">Election ID: ${electionId}</p>
                            </div>
                        </div>
                        <p class="mt-3">This will permanently delete:</p>
                        <ul>
                            <li>The election record</li>
                            <li>All votes cast in this election</li>
                            <li>All associated data</li>
                        </ul>
                        <p><strong>Type "DELETE" to confirm:</strong></p>
                        <input type="text" class="form-control" id="deleteConfirmInput" placeholder="Type DELETE to confirm">
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                        <button type="button" class="btn btn-danger" onclick="confirmDeleteElection('${electionId}')">
                            <i class="fas fa-trash"></i> Delete Election
                        </button>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    // Remove existing modal if any
    const existingModal = document.getElementById('deleteElectionModal');
    if (existingModal) {
        existingModal.remove();
    }
    
    // Add modal to body
    document.body.insertAdjacentHTML('beforeend', modalHtml);
    
    // Show modal
    const modal = new bootstrap.Modal(document.getElementById('deleteElectionModal'));
    modal.show();
}

// Confirm delete election
async function confirmDeleteElection(electionId) {
    const confirmInput = document.getElementById('deleteConfirmInput');
    
    if (confirmInput.value !== 'DELETE') {
        showAlert('Please type "DELETE" to confirm', 'warning');
        return;
    }
    
    const result = await apiCall('/admin/delete-election', {
        method: 'POST',
        body: JSON.stringify({ election_id: electionId })
    });
    
    if (result.success) {
        showAlert('Election deleted successfully!', 'success');
        
        // Hide modal
        const modal = bootstrap.Modal.getInstance(document.getElementById('deleteElectionModal'));
        modal.hide();
        
        loadElections();
        loadElectionStatus();
    } else {
        showAlert(result.message, 'danger');
    }
}

// View detailed election results
async function viewElectionResults(electionId) {
    try {
        const result = await apiCall(`/admin/election-details/${electionId}`);
        
        if (result.success) {
            showElectionResultsModal(result.results);
        } else {
            showAlert(result.message, 'danger');
        }
    } catch (error) {
        showAlert('Error loading election results: ' + error.message, 'danger');
    }
}

// Show election results modal
function showElectionResultsModal(results) {
    const election = results.election;
    const candidates = results.candidates;
    const totalVotes = results.total_votes;
    
    let candidatesHtml = '';
    if (candidates.length === 0) {
        candidatesHtml = '<div class="alert alert-info">No candidates or votes in this election.</div>';
    } else {
        candidates.forEach((candidate, index) => {
            const percentage = totalVotes > 0 ? ((candidate.votes / totalVotes) * 100).toFixed(1) : 0;
            const isWinner = index === 0 && candidate.votes > 0;
            
            candidatesHtml += `
                <div class="card mb-2 ${isWinner ? 'border-success' : ''}">
                    <div class="card-body py-2">
                        <div class="d-flex align-items-center justify-content-between">
                            <div class="d-flex align-items-center">
                                ${candidate.photo ? 
                                    `<img src="${candidate.photo}" alt="${candidate.name}" class="rounded-circle me-2" style="width: 40px; height: 40px; object-fit: cover;">` :
                                    `<div class="bg-secondary rounded-circle d-flex align-items-center justify-content-center text-white me-2" style="width: 40px; height: 40px;">
                                        <i class="fas fa-user"></i>
                                    </div>`
                                }
                                <div>
                                    <h6 class="mb-0">
                                        ${candidate.name}
                                        ${isWinner ? '<span class="badge bg-success ms-2">Winner</span>' : ''}
                                    </h6>
                                    <small class="text-muted">${percentage}% of votes</small>
                                </div>
                            </div>
                            <div class="text-end">
                                <h5 class="text-primary mb-0">${candidate.votes}</h5>
                                <small class="text-muted">votes</small>
                            </div>
                        </div>
                        <div class="progress mt-2" style="height: 6px;">
                            <div class="progress-bar ${isWinner ? 'bg-success' : ''}" style="width: ${percentage}%"></div>
                        </div>
                    </div>
                </div>
            `;
        });
    }
    
    const modalHtml = `
        <div class="modal fade" id="electionResultsModal" tabindex="-1">
            <div class="modal-dialog modal-lg">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">
                            <i class="fas fa-chart-bar"></i> Election Results: ${election.title}
                        </h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <div class="row mb-4">
                            <div class="col-md-4 text-center">
                                <h4 class="text-primary">${totalVotes}</h4>
                                <p class="mb-0">Total Votes</p>
                            </div>
                            <div class="col-md-4 text-center">
                                <h4 class="text-info">${candidates.length}</h4>
                                <p class="mb-0">Candidates</p>
                            </div>
                            <div class="col-md-4 text-center">
                                <h4 class="text-success">${election.status === 'ended' ? 'Completed' : 'Active'}</h4>
                                <p class="mb-0">Status</p>
                            </div>
                        </div>
                        
                        <div class="mb-3">
                            <h6>Election Details:</h6>
                            <p class="text-muted mb-1">${election.description}</p>
                            <small class="text-muted">
                                Created: ${new Date(election.created_at).toLocaleString()}<br>
                                ${election.started_at ? `Started: ${new Date(election.started_at).toLocaleString()}<br>` : ''}
                                ${election.ended_at ? `Ended: ${new Date(election.ended_at).toLocaleString()}` : ''}
                            </small>
                        </div>
                        
                        <h6>Results:</h6>
                        ${candidatesHtml}
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    // Remove existing modal if any
    const existingModal = document.getElementById('electionResultsModal');
    if (existingModal) {
        existingModal.remove();
    }
    
    // Add modal to body
    document.body.insertAdjacentHTML('beforeend', modalHtml);
    
    // Show modal
    const modal = new bootstrap.Modal(document.getElementById('electionResultsModal'));
    modal.show();
}

// Refresh results
async function refreshResults() {
    const result = await apiCall('/admin/results');
    
    if (result.success) {
        displayResults(result.results);
    } else {
        const container = document.getElementById('results-container');
        container.innerHTML = `
            <div class="alert alert-warning">
                ${result.message}
            </div>
        `;
    }
}

// Display results
function displayResults(results) {
    const container = document.getElementById('results-container');
    
    if (!results || !results.election) {
        container.innerHTML = `
            <div class="alert alert-info">
                No active election. Start an election to see results.
            </div>
        `;
        return;
    }
    
    const totalVotes = results.total_votes;
    const candidates = results.candidates;
    const election = results.election;
    
    let html = `
        <div class="row mb-4">
            <div class="col-md-4 text-center">
                <h3 class="text-primary">${totalVotes}</h3>
                <p class="mb-0">Total Votes</p>
            </div>
            <div class="col-md-4 text-center">
                <h3 class="text-info">${candidates.length}</h3>
                <p class="mb-0">Candidates</p>
            </div>
            <div class="col-md-4 text-center">
                <h3 class="text-success">${election.title}</h3>
                <p class="mb-0">Current Election</p>
            </div>
        </div>
    `;
    
    if (candidates.length === 0) {
        html += `
            <div class="alert alert-info">
                No candidates registered yet. Add candidates to see voting results.
            </div>
        `;
    } else {
        candidates.forEach((candidate, index) => {
            const percentage = totalVotes > 0 ? ((candidate.votes / totalVotes) * 100).toFixed(1) : 0;
            const isLeading = index === 0 && candidate.votes > 0;
            
            html += `
                <div class="card mb-3 ${isLeading ? 'border-success' : ''}">
                    <div class="card-body">
                        <div class="d-flex align-items-center justify-content-between">
                            <div class="d-flex align-items-center">
                                ${candidate.photo ? 
                                    `<img src="${candidate.photo}" alt="${candidate.name}" class="rounded-circle me-3" style="width: 50px; height: 50px; object-fit: cover;">` :
                                    `<div class="bg-secondary rounded-circle d-flex align-items-center justify-content-center text-white me-3" style="width: 50px; height: 50px;">
                                        <i class="fas fa-user"></i>
                                    </div>`
                                }
                                <div>
                                    <h6 class="mb-1">
                                        ${candidate.name}
                                        ${isLeading ? '<span class="badge bg-success ms-2">Leading</span>' : ''}
                                    </h6>
                                    <small class="text-muted">${percentage}% of votes</small>
                                </div>
                            </div>
                            <div class="text-end">
                                <h4 class="text-primary mb-0">${candidate.votes}</h4>
                                <small class="text-muted">votes</small>
                            </div>
                        </div>
                        <div class="progress mt-2" style="height: 8px;">
                            <div class="progress-bar ${isLeading ? 'bg-success' : ''}" style="width: ${percentage}%"></div>
                        </div>
                    </div>
                </div>
            `;
        });
    }
    
    container.innerHTML = html;
}

// Add candidate
async function addCandidate() {
    const nameInput = document.getElementById('candidate-name');
    const photoInput = document.getElementById('candidate-photo');
    
    const name = nameInput.value.trim();
    const photoUrl = photoInput.value.trim();
    
    if (!name) {
        showAlert('Please enter candidate name', 'warning');
        return;
    }
    
    const result = await apiCall('/admin/add-candidate', {
        method: 'POST',
        body: JSON.stringify({ 
            name: name, 
            photo_url: photoUrl 
        })
    });
    
    if (result.success) {
        showAlert('Candidate added successfully!', 'success');
        nameInput.value = '';
        photoInput.value = '';
        loadCandidates();
        refreshResults();
    } else {
        showAlert(result.message, 'danger');
    }
}

// Load candidates
async function loadCandidates() {
    const result = await apiCall('/admin/candidates');
    
    if (result.success) {
        const container = document.getElementById('candidates-list');
        
        if (result.candidates.length === 0) {
            container.innerHTML = '<p class="text-muted">No candidates added yet.</p>';
            return;
        }
        
        let html = '';
        result.candidates.forEach(candidate => {
            html += `
                <div class="candidate-item">
                    <div class="d-flex align-items-center justify-content-between">
                        <div class="d-flex align-items-center">
                            ${candidate.photo ? 
                                `<img src="${candidate.photo}" alt="${candidate.name}" class="rounded-circle me-3" style="width: 40px; height: 40px; object-fit: cover;">` :
                                `<div class="bg-secondary rounded-circle d-flex align-items-center justify-content-center text-white me-3" style="width: 40px; height: 40px;">
                                    <i class="fas fa-user"></i>
                                </div>`
                            }
                            <div>
                                <h6 class="mb-0">${candidate.name}</h6>
                                <small class="text-muted">ID: ${candidate.id}</small>
                            </div>
                        </div>
                        <button class="btn btn-sm btn-outline-danger" onclick="deleteCandidate('${candidate.id}', '${candidate.name}')">
                            <i class="fas fa-trash"></i>
                        </button>
                    </div>
                </div>
            `;
        });
        
        container.innerHTML = html;
    }
}

// Delete candidate
async function deleteCandidate(candidateId, candidateName) {
    if (!confirm(`Are you sure you want to delete candidate "${candidateName}"?`)) {
        return;
    }
    
    const result = await apiCall('/admin/delete-candidate', {
        method: 'POST',
        body: JSON.stringify({ candidate_id: candidateId })
    });
    
    if (result.success) {
        showAlert('Candidate deleted successfully!', 'success');
        loadCandidates();
        refreshResults();
    } else {
        showAlert(result.message, 'danger');
    }
}

// Add voter
async function addVoter() {
    const nameInput = document.getElementById('voter-name');
    const phoneInput = document.getElementById('voter-phone');
    const rollInput = document.getElementById('voter-roll');
    const emailInput = document.getElementById('voter-email');
    
    const name = nameInput.value.trim();
    const phone = phoneInput.value.trim();
    const roll = rollInput.value.trim();
    const email = emailInput.value.trim();
    
    if (!name || !phone || !roll || !email) {
        showAlert('Please fill all fields', 'warning');
        return;
    }
    
    const result = await apiCall('/admin/add-voter', {
        method: 'POST',
        body: JSON.stringify({ 
            name: name,
            phone: phone,
            roll_number: roll,
            email: email
        })
    });
    
    if (result.success) {
        showAlert('Voter added successfully!', 'success');
        nameInput.value = '';
        phoneInput.value = '';
        rollInput.value = '';
        emailInput.value = '';
        loadVoters();
    } else {
        showAlert(result.message, 'danger');
    }
}

// Edit voter
async function editVoter(phone) {
    try {
        // Get all voters to find the one to edit
        const result = await apiCall('/admin/voters');
        
        if (result.success) {
            const voter = result.voters.find(v => v.phone === phone);
            if (voter) {
                showEditVoterModal(voter);
            }
        }
    } catch (error) {
        showAlert('Error loading voter details: ' + error.message, 'danger');
    }
}

// Show edit voter modal
function showEditVoterModal(voter) {
    const modalHtml = `
        <div class="modal fade" id="editVoterModal" tabindex="-1">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title"><i class="fas fa-edit"></i> Edit Voter</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <div class="mb-3">
                            <label for="edit-voter-name" class="form-label">Full Name</label>
                            <input type="text" class="form-control" id="edit-voter-name" value="${voter.name}">
                        </div>
                        <div class="mb-3">
                            <label for="edit-voter-phone" class="form-label">Phone Number</label>
                            <input type="tel" class="form-control" id="edit-voter-phone" value="${voter.phone.replace('+91', '')}">
                        </div>
                        <div class="mb-3">
                            <label for="edit-voter-roll" class="form-label">Roll Number / Voter ID</label>
                            <input type="text" class="form-control" id="edit-voter-roll" value="${voter.roll_number}">
                        </div>
                        <div class="mb-3">
                            <label for="edit-voter-email" class="form-label">Email</label>
                            <input type="email" class="form-control" id="edit-voter-email" value="${voter.email}">
                        </div>
                        <div class="alert alert-info">
                            <i class="fas fa-info-circle"></i>
                            <strong>Status:</strong> ${voter.has_voted ? 'Has voted in current election' : 'Has not voted yet'}
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                        <button type="button" class="btn btn-primary" onclick="updateVoter('${voter.phone}')">
                            <i class="fas fa-save"></i> Update Voter
                        </button>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    // Remove existing modal if any
    const existingModal = document.getElementById('editVoterModal');
    if (existingModal) {
        existingModal.remove();
    }
    
    // Add modal to body
    document.body.insertAdjacentHTML('beforeend', modalHtml);
    
    // Show modal
    const modal = new bootstrap.Modal(document.getElementById('editVoterModal'));
    modal.show();
}

// Update voter
async function updateVoter(originalPhone) {
    const name = document.getElementById('edit-voter-name').value.trim();
    const phone = document.getElementById('edit-voter-phone').value.trim();
    const rollNumber = document.getElementById('edit-voter-roll').value.trim();
    const email = document.getElementById('edit-voter-email').value.trim();
    
    if (!name || !phone || !rollNumber || !email) {
        showAlert('All fields are required', 'warning');
        return;
    }
    
    try {
        const result = await apiCall('/admin/update-voter', {
            method: 'POST',
            body: JSON.stringify({
                original_phone: originalPhone,
                name: name,
                phone: phone,
                roll_number: rollNumber,
                email: email
            })
        });
        
        if (result.success) {
            showAlert(result.message, 'success');
            
            // Hide modal
            const modal = bootstrap.Modal.getInstance(document.getElementById('editVoterModal'));
            modal.hide();
            
            // Refresh voters list
            loadVoters();
        } else {
            showAlert(result.message, 'danger');
        }
    } catch (error) {
        showAlert('Error updating voter: ' + error.message, 'danger');
    }
}

// Delete voter
async function deleteVoter(phone, name) {
    if (!confirm(`Are you sure you want to delete voter "${name}"?\n\nThis action cannot be undone.`)) {
        return;
    }
    
    try {
        const result = await apiCall('/admin/delete-voter', {
            method: 'POST',
            body: JSON.stringify({ phone: phone })
        });
        
        if (result.success) {
            showAlert(result.message, 'success');
            loadVoters();
        } else {
            showAlert(result.message, 'danger');
        }
    } catch (error) {
        showAlert('Error deleting voter: ' + error.message, 'danger');
    }
}

// Load and display all voters
async function loadVoters() {
    try {
        const container = document.getElementById('voters-list');
        container.innerHTML = '<div class="text-center"><div class="spinner-border spinner-border-sm" role="status"></div> Loading voters...</div>';
        
        const result = await apiCall('/admin/voters');
        
        if (result.success) {
            displayVoters(result.voters);
        } else {
            container.innerHTML = `<div class="alert alert-danger">${result.message}</div>`;
        }
    } catch (error) {
        document.getElementById('voters-list').innerHTML = `<div class="alert alert-danger">Error loading voters: ${error.message}</div>`;
    }
}

// Display voters in the list
function displayVoters(voters) {
    const container = document.getElementById('voters-list');
    
    if (voters.length === 0) {
        container.innerHTML = '<p class="text-muted text-center">No voters registered yet.</p>';
        return;
    }
    
    const votersHtml = voters.map(voter => `
        <div class="voter-item">
            <div class="d-flex justify-content-between align-items-start">
                <div class="flex-grow-1">
                    <h6 class="mb-1">${voter.name}</h6>
                    <small class="text-muted">
                        <i class="fas fa-id-card"></i> ${voter.roll_number} | 
                        <i class="fas fa-phone"></i> ${voter.phone} | 
                        <i class="fas fa-envelope"></i> ${voter.email}
                    </small>
                    <div class="mt-1">
                        <span class="badge ${voter.has_voted ? 'bg-success' : 'bg-secondary'}">
                            ${voter.has_voted ? 'Voted' : 'Not Voted'}
                        </span>
                        ${voter.photo ? '<span class="badge bg-info ms-1">Has Photo</span>' : ''}
                    </div>
                </div>
                <div class="btn-group btn-group-sm">
                    <button class="btn btn-outline-primary" onclick="editVoter('${voter.phone}')" title="Edit">
                        <i class="fas fa-edit"></i>
                    </button>
                    <button class="btn btn-outline-danger" onclick="deleteVoter('${voter.phone}', '${voter.name}')" title="Delete">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
            </div>
        </div>
    `).join('');
    
    container.innerHTML = votersHtml;
}

// Load voters from Excel
async function uploadVotersFromExcel() {
    const fileInput = document.getElementById('voters-file');
    const file = fileInput.files[0];
    
    if (!file) {
        showAlert('Please select an Excel file', 'warning');
        return;
    }
    
    const formData = new FormData();
    formData.append('file', file);
    
    try {
        const response = await fetch('/admin/load-voters', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        
        if (result.success) {
            showAlert(result.message, 'success');
            fileInput.value = '';
        } else {
            showAlert(result.message, 'danger');
        }
    } catch (error) {
        showAlert('Error uploading file: ' + error.message, 'danger');
    }
}

// Load past elections summary
async function loadPastElectionsSummary() {
    try {
        const result = await apiCall('/admin/elections');
        
        if (result.success) {
            const container = document.getElementById('past-elections-summary');
            const pastElections = result.elections.filter(e => e.status === 'ended');
            
            if (pastElections.length === 0) {
                container.innerHTML = '<p class="text-muted text-center">No completed elections yet.</p>';
                return;
            }
            
            let html = '';
            pastElections.slice(0, 5).forEach(election => { // Show last 5 elections
                const endedDate = new Date(election.ended_at).toLocaleDateString();
                const totalVotes = election.total_votes || 0;
                
                html += `
                    <div class="border rounded p-2 mb-2">
                        <div class="d-flex justify-content-between align-items-center">
                            <div>
                                <h6 class="mb-1">${election.title}</h6>
                                <small class="text-muted">
                                    Ended: ${endedDate} | Votes: ${totalVotes}
                                </small>
                            </div>
                            <button class="btn btn-sm btn-outline-info" onclick="viewElectionResults('${election.id}')" title="View Details">
                                <i class="fas fa-eye"></i>
                            </button>
                        </div>
                    </div>
                `;
            });
            
            if (pastElections.length > 5) {
                html += `<p class="text-muted text-center mt-2">Showing 5 most recent elections</p>`;
            }
            
            container.innerHTML = html;
        }
    } catch (error) {
        document.getElementById('past-elections-summary').innerHTML = 
            `<div class="alert alert-danger">Error loading past elections: ${error.message}</div>`;
    }
}

// Auto-refresh results every 30 seconds
setInterval(() => {
    if (!document.getElementById('admin-dashboard').classList.contains('d-none')) {
        refreshResults();
        loadElectionStatus();
        loadPastElectionsSummary();
    }
}, 30000);