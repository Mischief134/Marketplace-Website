const productInfoForm = {
    delimiters: ['[[', ']]'],
    template: `<b-form ref="form">
        {% csrf_token %}
        <b-form-group
            label="Name:"
            label-for="product-title"
        >
            <b-form-input
                id="product-title"
                v-model="title"
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
                    v-model="price"
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
                v-model="description"
                :state="descriptionState"
                placeholder="Say something about your product..."
                rows="8"
                required
            ></b-form-textarea>
            <b-form-invalid-feedback :state="descriptionState">
                [[ error.description ]]
            </b-form-invalid-feedback>
        </b-form-group>
        <b-form-group
            label="Product image:"
            label-for="product-image"
        >
            <b-form-file
                id="product-image"
                v-model="image"
                :state="imageState"
                accept="image/*"
            ></b-form-file>
            <b-form-invalid-feedback :state="imageState">
                [[ error.image ]]
            </b-form-invalid-feedback>
        </b-form-group>
    </b-form>
    `,
    props: {
        data: {
            type: Object,
            default: null,
            validator: obj => obj.hasOwnProperty('title') && obj.hasOwnProperty('price')
                                && obj.hasOwnProperty('description'),
        },
        error: {
            type: Object,
            validator: obj => obj.hasOwnProperty('title') && obj.hasOwnProperty('price')
                                && obj.hasOwnProperty('description') && obj.hasOwnProperty('image'),
        },
    },
    data() {
        return {
            title: '',
            price: '0.00',
            description: '',
            image: null,
        };
    },
    watch: {
        data(newData) {
            if (newData) {
                this.setData(newData);
            }
        },
    },
    created() {
        if (this.data) {
            this.setData(this.data);
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
        imageState() {
            if (this.error.image != '') return false;
            return null;
        },
    },
    methods: {
        initialize() {
            this.title = '';
            this.price = '0.00';
            this.description = '';
            this.image = null;
        },
        setData(data) {
            if (!(data.hasOwnProperty('title') || data.hasOwnProperty('price') || data.hasOwnProperty('description'))) {
                throw new Error('Missing required attribute(s).')
            }
            this.title = data.title;
            this.price = data.price;
            this.description = data.description;
        },
        getFormData() {
            const formData = new FormData(this.$refs.form);
            formData.set('title', this.title);
            formData.set('price', Number(this.price));
            formData.set('description', this.description);
            formData.set('image', this.image);
            return formData;
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
};