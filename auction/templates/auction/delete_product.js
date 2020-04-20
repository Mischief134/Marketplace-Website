Vue.component('delete-product-form', {
    delimiters: ['[[', ']]'],
    template: `<b-modal id="delete-conformation" v-model="deleteModal" title="Delete listing">
        Are you sure you want to delete this listing?
        <template v-slot:modal-footer="{ cancel }">
            <b-button @click="cancel">Cancel</b-button>
            <b-button variant="danger" @click="deleteProduct">Yes</b-button>
        </template>
        {% csrf_token %}
    </b-modal>
    `,
    data() {
        return {
            id: -1,
            deleteModal: false,
        };
    },
    methods: {
        openDeleteModal(id) {
            this.id = id;
            this.deleteModal = true;
        },
        deleteProduct() {
            const csrfToken = document.getElementsByName('csrfmiddlewaretoken')[0].value;
            axios.post(`/auction/${this.id}/delete/`, {}, {
                headers: {
                    'X-CSRFToken': csrfToken,
                },
            }).then(() => {
                window.location.reload();
            });
        },
    },
});