
function confirmarExclusao(event) {
    if (!confirm('Deseja realmente excluir este registro?')) {
        event.preventDefault();
    }
}

document.querySelectorAll('.btn-danger').forEach(btn => {
    btn.addEventListener('click', confirmarExclusao);
});
