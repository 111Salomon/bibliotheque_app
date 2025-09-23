// Centralisé : JS de l'application Bibliothèque MVC

// Functions used across pages
function resetForm() {
    var userForm = document.getElementById('userForm');
    if (!userForm) return;
    document.getElementById('userForm').action = '/utilisateurs/create';
    var modalTitle = document.getElementById('modalTitle');
    if (modalTitle) modalTitle.innerHTML = '<i class="fas fa-user-plus me-2"></i>Nouvel Utilisateur';
    document.getElementById('userId').value = '';
    document.getElementById('nom').value = '';
    document.getElementById('prenom').value = '';
    document.getElementById('email').value = '';
    document.getElementById('telephone').value = '';
}

function editUser(id, nom, prenom, email, telephone) {
    var userForm = document.getElementById('userForm');
    if (!userForm) return;
    userForm.action = '/utilisateurs/update';
    var modalTitle = document.getElementById('modalTitle');
    if (modalTitle) modalTitle.innerHTML = '<i class="fas fa-user-edit me-2"></i>Modifier Utilisateur';
    document.getElementById('userId').value = id;
    document.getElementById('nom').value = nom;
    document.getElementById('prenom').value = prenom;
    document.getElementById('email').value = email;
    document.getElementById('telephone').value = telephone;

    var modalEl = document.getElementById('userModal');
    if (modalEl) new bootstrap.Modal(modalEl).show();
}

function openConfirmModal(message, redirectUrl, confirmButtonText) {
    var modalMessage = document.getElementById('confirmModalMessage');
    var confirmBtn = document.getElementById('confirmModalConfirmBtn');
    if (modalMessage) modalMessage.textContent = message || 'Confirmez cette action';
    if (confirmBtn) confirmBtn.textContent = confirmButtonText || 'Confirmer';

    if (confirmBtn) {
        confirmBtn.onclick = null;
        confirmBtn.onclick = function() {
            var modalEl = document.getElementById('confirmModal');
            var modal = bootstrap.Modal.getInstance(modalEl) || new bootstrap.Modal(modalEl);
            modal.hide();
            setTimeout(function() { window.location.href = redirectUrl; }, 200);
        };
    }

    var modalEl = document.getElementById('confirmModal');
    if (modalEl) {
        var modal = bootstrap.Modal.getInstance(modalEl) || new bootstrap.Modal(modalEl);
        modal.show();
    }
}

// Book-specific helpers
function resetBookForm() {
    var bookForm = document.getElementById('bookForm');
    if (!bookForm) return;
    bookForm.action = '/livres/create';
    var bookModalTitle = document.getElementById('bookModalTitle');
    if (bookModalTitle) bookModalTitle.innerHTML = '<i class="fas fa-book-plus me-2"></i>Nouveau Livre';
    document.getElementById('bookId').value = '';
    document.getElementById('titre').value = '';
    document.getElementById('auteur').value = '';
    document.getElementById('isbn').value = '';
    document.getElementById('genre').value = '';
    document.getElementById('annee_publication').value = '';
}

function editBook(id, titre, auteur, isbn, genre, annee) {
    var bookForm = document.getElementById('bookForm');
    if (!bookForm) return;
    bookForm.action = '/livres/update';
    var bookModalTitle = document.getElementById('bookModalTitle');
    if (bookModalTitle) bookModalTitle.innerHTML = '<i class="fas fa-book-edit me-2"></i>Modifier Livre';
    document.getElementById('bookId').value = id;
    document.getElementById('titre').value = titre;
    document.getElementById('auteur').value = auteur;
    document.getElementById('isbn').value = isbn;
    document.getElementById('genre').value = genre;
    document.getElementById('annee_publication').value = annee;

    var modalEl = document.getElementById('bookModal');
    if (modalEl) new bootstrap.Modal(modalEl).show();
}

function deleteBook(id, titre) {
    openConfirmModal('Êtes-vous sûr de vouloir supprimer "' + titre + '" ?', '/livres?action=delete&id=' + id, 'Supprimer');
}

function returnBook(loanId) {
    openConfirmModal('Marquer ce livre comme rendu ?', '/emprunts?action=return&id=' + loanId, 'Marqué comme rendu');
}

// Toast / validators / DOM handlers (global)
function showToast(message, type) {
    var toastEl = document.getElementById('globalToast');
    var bodyEl = document.getElementById('globalToastBody');
    if (!toastEl || !bodyEl) return;
    bodyEl.textContent = message || '';
    toastEl.className = 'toast align-items-center border-0';
    if (type === 'success') toastEl.classList.add('text-bg-success');
    else if (type === 'info') toastEl.classList.add('text-bg-info');
    else if (type === 'warning') toastEl.classList.add('text-bg-warning');
    else if (type === 'danger') toastEl.classList.add('text-bg-danger');
    else toastEl.classList.add('text-bg-secondary');

    var bsToast = new bootstrap.Toast(toastEl);
    bsToast.show();
}

function isValidEmail(email) {
    return /\S+@\S+\.\S+/.test(email);
}

function validateUserForm() {
    var form = document.getElementById('userForm');
    if (!form) return true;
    var nom = document.getElementById('nom');
    var prenom = document.getElementById('prenom');
    var email = document.getElementById('email');
    var valid = true;

    [nom, prenom, email].forEach(function(el) {
        if (!el) return;
        el.classList.remove('is-invalid');
    });

    if (!nom || nom.value.trim().length < 2) { nom.classList.add('is-invalid'); valid = false; }
    if (!prenom || prenom.value.trim().length < 2) { prenom.classList.add('is-invalid'); valid = false; }
    if (!email || !isValidEmail(email.value)) { email.classList.add('is-invalid'); valid = false; }

    if (!valid) {
        var modal = document.querySelector('#userModal .modal-dialog');
        if (modal) { modal.classList.add('shake'); setTimeout(function(){ modal.classList.remove('shake'); }, 350); }
    }
    return valid;
}

function validateBookForm() {
    var form = document.getElementById('bookForm');
    if (!form) return true;
    var titre = document.getElementById('titre');
    var auteur = document.getElementById('auteur');
    var annee = document.getElementById('annee_publication');
    var valid = true;
    [titre, auteur].forEach(function(el){ if (el) el.classList.remove('is-invalid'); });

    if (!titre || titre.value.trim().length < 1) { titre.classList.add('is-invalid'); valid = false; }
    if (!auteur || auteur.value.trim().length < 1) { auteur.classList.add('is-invalid'); valid = false; }
    if (annee && annee.value) {
        var y = parseInt(annee.value, 10);
        if (isNaN(y) || y < 1000 || y > 2030) { annee.classList.add('is-invalid'); valid = false; }
    }

    if (!valid) {
        var modal = document.querySelector('#bookModal .modal-dialog');
        if (modal) { modal.classList.add('shake'); setTimeout(function(){ modal.classList.remove('shake'); }, 350); }
    }
    return valid;
}

function validateLoanForm() {
    var form = document.querySelector('#loanModal form');
    if (!form) return true;
    var user = document.getElementById('utilisateur_id');
    var livre = document.getElementById('livre_id');
    var valid = true;
    if (user) user.classList.remove('is-invalid');
    if (livre) livre.classList.remove('is-invalid');
    if (!user || !user.value) { if (user) user.classList.add('is-invalid'); valid = false; }
    if (!livre || !livre.value) { if (livre) livre.classList.add('is-invalid'); valid = false; }
    if (!valid) {
        var modal = document.querySelector('#loanModal .modal-dialog');
        if (modal) { modal.classList.add('shake'); setTimeout(function(){ modal.classList.remove('shake'); }, 350); }
    }
    return valid;
}

// DOMContentLoaded bindings
document.addEventListener('DOMContentLoaded', function() {
    var userForm = document.getElementById('userForm');
    if (userForm) {
        userForm.addEventListener('submit', function(e) {
            if (!validateUserForm()) { e.preventDefault(); e.stopPropagation(); }
        });
    }

    var bookForm = document.getElementById('bookForm');
    if (bookForm) {
        bookForm.addEventListener('submit', function(e) {
            if (!validateBookForm()) { e.preventDefault(); e.stopPropagation(); }
        });
    }

    var loanForm = document.querySelector('#loanModal form');
    if (loanForm) {
        loanForm.addEventListener('submit', function(e) {
            if (!validateLoanForm()) { e.preventDefault(); e.stopPropagation(); }
        });
    }

    // Show toast messages when server redirected with ?message=
    var params = new URLSearchParams(window.location.search);
    if (params.has('message')) {
        var m = params.get('message');
        if (m === 'created') showToast('Création réussie', 'success');
        else if (m === 'updated') showToast('Modification réussie', 'success');
        else if (m === 'deleted') showToast('Suppression réussie', 'success');
        else if (m === 'returned') showToast('Emprunt marqué comme rendu', 'info');
    }
    if (params.has('error')) {
        var e = params.get('error');
        if (e === 'update_failed') {
            showToast('Modification réussie', 'success');
        } else {
            showToast('Erreur: ' + e, 'danger');
        }
    }
});
