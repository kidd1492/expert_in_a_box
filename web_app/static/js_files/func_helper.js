function toggleSelectAll() {
    const checked = document.getElementById("select-all").checked;
    document.querySelectorAll(".doc-checkbox").forEach(cb => cb.checked = checked);
}

function getSelectedDocuments() {
    const selected = [];
    document.querySelectorAll(".doc-checkbox:checked").forEach(cb => {
        selected.push(cb.value);
    });
    return selected;
}

