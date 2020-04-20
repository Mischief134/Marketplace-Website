Vue.component('add-product-form', {
    delimiters: ['[[', ']]'],
    components: {
        'product-info-form': productInfoForm,
    },
    template: `
        <b-modal v-model="createModal" title="Add new listing">
            <product-info-form ref="form" :error="error"></product-info-form>
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
    props: {
        value: Boolean,
    },
    data() {
        return {
            createModal: this.value,
            error: {
                title: '',
                price: '',
                description: '',
                image: '',
            },
        }
    },
    watch: {
        value(newVal) {
            this.createModal = newVal;
        },
        createModal(newVal) {
            this.$emit('input', newVal);
        },
    },
    methods: {
        initialize() {
            this.error = {
                title: '',
                price: '',
                description: '',
                image: '',
            };
            this.$refs.form.initialize();
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

            axios.post('/auction/create/', formData).then(() => {
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