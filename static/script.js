document.addEventListener('DOMContentLoaded', function() {
    const items = document.querySelectorAll('.item');

    items.forEach(item => {
        item.addEventListener('mouseover', function() {
            const tooltipText = this.getAttribute('data-tooltip');
            const tooltip = document.getElementById('tooltip');
            const rarityColor = this.getAttribute('data-rarity-color');

	    // Create HTML for multiple lines in the tooltip with specific classes
            const lines = tooltipText.split('\n');
	    const tooltipHTML = lines.map((line, index) => {
                if (index === 0) {
                    return `<p class="rarity-text" style="color: ${rarityColor};">${line}</p>`;
                } else if (index === 1) {
                    return `<p>${line}</p>`;
                } else {
                    return `<p class="blue-text">${line}</p>`;
                }
            }).join('');
	
	    tooltip.innerHTML = tooltipHTML;
            tooltip.style.display = 'block';

            // Position the tooltip
            const rect = this.getBoundingClientRect();
            const scrollTop = document.documentElement.scrollTop || document.body.scrollTop;
            tooltip.style.top = scrollTop + rect.top + 'px';
            tooltip.style.left = rect.left + rect.width + 'px';
        });

        item.addEventListener('mouseout', function() {
            const tooltip = document.getElementById('tooltip');
            tooltip.style.display = 'none';
        });
    });
});

document.addEventListener('DOMContentLoaded', function() {
   const tabs = document.querySelectorAll('.tab');
   tabs.forEach(tab => {
        tab.addEventListener('click', function() {
            const inactive_tabs = document.querySelectorAll('.tab');
            inactive_tabs.forEach(inactive_tab => {
                inactive_tab.classList.remove('active');
            });
            this.classList.add('active');

            const stashes = document.querySelectorAll('.stash');
            stashes.forEach(stash => {
                stash.style.display = 'none';
            });

            const active_stash = this.getAttribute('data-stash');
            const stash  = document.getElementById(active_stash);
            stash.style.display = 'grid';
        });
    });
   // $('.tab').click(function(){
   //      // Hide all stashes
   //      $('.stash').hide();
   //      // Remove active class from all tabs
   //      $('.tab').removeClass('active');
   //      // Get the corresponding stash ID from the data attribute
   //      var stashId = $(this).data('stash');
   //      // Show the clicked stash and add active class to the clicked tab
   //      $('#' + stashId).show();
   //      $(this).addClass('active');
   //  });
});
