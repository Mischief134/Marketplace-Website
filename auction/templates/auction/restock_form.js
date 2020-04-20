Vue.component('restock-form', {
    delimiters: ['[[', ']]'],
    template: `<b-modal id="restock-modal" title="Restock Item" v-model="showModal">
        <p>You are restocking <strong>[[ itemName ]]</strong></p>
        <b-form ref="form">
            {% csrf_token %}
            <b-form-group
                label="Restock quantity:"
                label-for="restock-quantity"
            >
                <b-form-input
                    id="restock-quantity"
                    v-model="form.quantity"
                    required
                    :state="restockQuantityState"
                    type="number"
                    min="1"
                ></b-form-input>
            </b-form-group>
        </b-form>
        <template v-slot:modal-footer="{ ok, cancel }">
            <b-button variant="outline-secondary" @click="cancelRestock">
                Cancel
            </b-button>
            <b-button variant="outline-primary" type="submit" @click="submitRestockForm">
                Submit
            </b-button>
        </template>
    </b-modal>`,
    props: {
        itemName: {
            type: String,
            default: "",
        },
    },
    data() {
        return {
            showModal: this.value,
            itemId: -1,
            form: {
                quantity: 1,
            },
        }
    },
    watch: {
        showModal(show) {
            if (!show) {
                this.itemId = -1;
                this.form.quantity = 1;
            }
        }
    },
    computed: {
        restockQuantityState() {
            if (this.form.quantity < 1) return false;
            return true;
        },
    },
    methods: {
        openRestockForm(id) {
            this.itemId = id;
            this.showModal = true;
        },
        cancelRestock() {
            this.showModal = false;
            this.$emit('close');
        },
        submitRestockForm() {
            if (this.restockQuantityState) {
                axios.post(`/auction/${this.itemId}/restock/`, {
                    amount: Number(this.form.quantity),
                }, {
                    headers: { 'X-CSRFToken': this.$refs.form.elements['csrfmiddlewaretoken'].value }
                }).then(() => {
                    window.location.reload();
                });
            }
            this.$emit('close');
        },
    },
});