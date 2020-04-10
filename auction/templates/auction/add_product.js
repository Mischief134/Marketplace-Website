Vue.component('add-product', {
    delimiters: ['[[', ']]'],
    template: `
        <b-modal v-model="createModal" title="Add new listing">
            <b-form ref="form">
                {% csrf_token %}
                <b-form-group
                    label="Name:"
                    label-for="product-title"
                >
                    <b-form-input
                        id="product-title"
                        v-model="form.title"
                        :state="titleState"
                        required
                        placeholder="Ex. Sweet Awesome Headphones"
                    ></b-form-input>
                    <b-form-invalid-feedback :state="titleState">
                        [[ error.title ]]
                    </b-form-invalid-feedback>
                </b-form-group>
                <b-form-group
                    label="Price:"
                    label-for="product-price"
                >
                    <b-input-group prepend="$">
                        <b-form-input
                            id="product-price"
                            v-model="form.price"
                            :state="priceState"
                            required type="number" step="0.01"
                            min="0.00" lazy-formatter
                            :formatter="formatPrice"
                        ></b-form-input>
                    </b-input-group>
                    <b-form-invalid-feedback :state="priceState">
                        [[ error.price ]]
                    </b-form-invalid-feedback>
                </b-form-group>
                <b-form-group
                    label="Product description:"
                    label-for="product-description"
                >
                    <b-form-textarea
                        id="product-description"
                        v-model="form.description"
                        :state="descriptionState"
                        placeholder="Say something about your product..."
                        rows="8"
                        required
                    ></b-form-textarea>
                    <b-form-invalid-feedback :state="descriptionState">
                        [[ error.description ]]
                    </b-form-invalid-feedback>
                </b-form-group>
            </b-form>
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
            form: {
                title: '',
                price: '0.00',
                description: '',
            },
            error: {
                title: '',
                price: '',
                description: '',
            },
        }
    },
    computed: {
        titleState() {
            if (this.error.title != '') return false;
            return null;
        },
        priceState() {
            if (this.error.price != '') return false;
            return null;
        },
        descriptionState() {
            if (this.error.description != '') return false;
            return null;
        },
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
        submitForm() {
            this.error = {
                title: '',
                price: '',
                description: '',
            };
            axios.post('/auction/create/', {
                title: this.form.title,
                price: Number(this.form.price),
                description: this.form.description,
            }, {
                headers: {
                    'X-CSRFToken': this.$refs.form.elements['csrfmiddlewaretoken'].value
                }
            }).then(() => {
                this.createModal = false;
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
                }
            });
        },
        formatPrice(value) {
            const numStr = String(Math.round(Number(value) * 100) / 100);
            const parts = numStr.split('.');
            // Pad the string
            if (parts.length < 2) {
                return numStr + '.00';
            } else if (parts[1].length < 2) {
                return numStr + '0';
            }
            return numStr;
        }
    }
});