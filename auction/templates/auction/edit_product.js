Vue.component('edit-product-form', {
    delimiters: ['[[', ']]'],
    components: {
        'product-info-form': productInfoForm,
    },
    template: `
        <b-modal v-model="updateModal" title="Edit listing">
            <product-info-form ref="form" :data="form" :error="error"></product-info-form>
            <template v-slot:modal-footer="{ ok, cancel }">
                <b-button variant="outline-secondary" @click="cancel">
                    Cancel
                </b-button>
                <b-button variant="outline-primary" type="submit" @click="submitForm">
                    Submit
                </b-button>
            </template>
        </b-modal>
    `,
    data() {
        return {
            updateModal: this.value,
            id: -1,
            form: null,
            error: {
                title: '',
                price: '',
                description: '',
                image: '',
            },
        }
    },
    watch: {
        updateModal(toShow) {
            if (!toShow) {
                this.initialize();
            }
        },
    },
    methods: {
        initialize() {
            this.id = -1,
            this.error = {
                title: '',
                price: '',
                description: '',
                image: '',
            };
            this.$refs.form.initialize();
        },
        openUpdateModal(id) {
            this.id = id;
            axios.get(`/auction/${this.id}/info/`).then((res) => {
                this.form = res.data.product;
                this.updateModal = true;
            });
        },
        submitForm() {
            this.error = {
                title: '',
                price: '',
                description: '',
                image: '',
            };

            // Create a new FormData object to be posted to the server
            const formData = this.$refs.form.getFormData();

            axios.post(`/auction/${this.id}/info/`, formData).then(() => {
                window.location.reload();
            }).catch((err) => {
                if (err.response.data.hasOwnProperty('errors')) {
                    const msg = err.response.data.errors;
                    if (msg.hasOwnProperty('title')) {
                        [this.error.title] = msg.title;
                    }
                    if (msg.hasOwnProperty('price')) {
                        [this.error.price] = msg.price;
                    }
                    if (msg.hasOwnProperty('description')) {
                        [this.error.description] = msg.description;
                    }
                    if (msg.hasOwnProperty('image')) {
                        [this.error.image] = msg.image;
                    }
                }
            });
        },
    }
});