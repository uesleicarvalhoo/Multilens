from flask_wtf import FlaskForm
from wtforms import FloatField, PasswordField, StringField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.fields.html5 import EmailField
from wtforms.validators import Email, Length, Optional, Regexp, Required

from multilens.ext.db.models import (PaymentType, Register, SaleType,
                                     Speciality, Storage)


class BaseForm(FlaskForm):
    def populate_obj(self, obj: FlaskForm):
        super(FlaskForm, self).populate_obj(obj)
        for field in self:
            if isinstance(field, QuerySelectField):
                setattr(obj, field.name, field.data.id)


class FormLogin(BaseForm):
    username = StringField("Usuario", [Required()])
    passwd = PasswordField("Senha", [Required()])


class FormDoctor(BaseForm):
    name = StringField(
        "Nome",
        [
            Required("Informe o nome"),
            Length(min=5, max=50, message="O nome deve conter de 5 a 50 caracters"),
        ],
    )
    cpf = StringField(
        "CPF",
        [
            Required("Informe o CPF"),
            Length(min=11, max=11, message="O CPF deve conter exatamente 11 números"),
            Regexp("^[0-9]*$", message="Informe somente números"),
        ],
    )
    rg = StringField(
        "RG",
        [
            Required("Informe o RG"),
            Length(min=10, max=10, message="O RG precisa conter exatamente 10 números"),
            Regexp("^[0-9]*$", message="Informe somente números"),
        ],
    )
    crm = StringField(
        "CRM",
        [
            Required("Informe o CRM"),
            Length(min=5, max=12, message="O CRM precisa conter de 5 a 12 números"),
            Regexp("^[0-9]*$", message="Informe somente números"),
        ],
    )
    cel = StringField(
        "Celular",
        [
            Required("Informe um número de celular valido"),
            Length(
                min=11, max=11, message="O celular precisa conter exatamente 11 números"
            ),
            Regexp("^[0-9]*$", message="Informe somente números"),
        ],
    )
    phone = StringField(
        "Telefone",
        [
            Required("Informe um telefone validio"),
            Length(
                min=10,
                max=10,
                message="O telefone precisa conter exatamente 10 números",
            ),
            Regexp("^[0-9]*$", message="Informe somente números"),
        ],
    )
    email = EmailField(
        "Email", [Required("Informe o Email"), Email("Informe um e-mail valido")]
    )
    speciality_id = QuerySelectField(
        "Especialidade",
        [Required("Selecione a especialidade")],
        get_label="speciality",
        get_pk=lambda x: x.id,
        query_factory=lambda: Speciality.query,
        allow_blank=True,
    )
    zip = StringField(
        "CEP",
        [
            Required("Informe um CEP valido"),
            Length(
                min=8, max=8, message="O CEP precisa conter exatamente 8 caracters."
            ),
            Regexp("^[0-9]*$", message="Informe somente números"),
        ],
    )
    city = StringField("Cidade", [Required("Informe uma cidade")])
    address = StringField(
        "Endereço",
        [
            Required("Informe o endereço"),
            Length(
                min=1, max=70, message="O endereço precisa ter no máximo 70 caracters"
            ),
        ],
    )
    district = StringField(
        "Bairro",
        [
            Required("Informe o bairro"),
        ],
    )

    def load(self, doctor):
        self.process(obj=doctor)

        if doctor.register is not None:
            self.speciality_id.data = doctor.speciality
            self.zip.data = doctor.register.zip
            self.address.data = doctor.register.address
            self.city.data = doctor.register.city
            self.district.data = doctor.register.district


class FormInstitution(BaseForm):
    name = StringField("Nome", [Required("O nome da instituição é obrigatorio")])
    cnpj = StringField(
        "CNPJ",
        [
            Required("O CNPJ é obrigatório"),
            Regexp("^[0-9]*$", message="Informe somente números"),
        ],
    )
    adm_name = StringField("Administração")
    adm_email = EmailField("Adm. Email", [Optional(), Email("Informe um email valido")])
    adm_cel = StringField(
        "Adm. Celular",
        [
            Optional(),
            Regexp("^[0-9]*$", message="Informe somente números"),
            Length(
                min=11, max=11, message="O celular precisa conter exatamente 11 números"
            ),
        ],
    )
    adm_phone = StringField(
        "Adm. Telefone",
        [
            Optional(),
            Regexp("^[0-9]*$", message="Informe somente números"),
            Length(
                min=10,
                max=10,
                message="O telefone precisa conter exatamente 10 números",
            ),
        ],
    )
    enf_name = StringField("Enfermagem")
    enf_email = EmailField("Enf. Email", [Optional(), Email("Informe um email valido")])
    enf_cel = StringField(
        "Enf. Celular",
        [
            Optional(),
            Regexp("^[0-9]*$", message="Informe somente números"),
            Length(
                min=11, max=11, message="O celular precisa conter exatamente 11 números"
            ),
        ],
    )
    enf_phone = StringField(
        "Enf. Telefone",
        [
            Optional(),
            Regexp("^[0-9]*$", message="Informe somente números"),
            Length(
                min=10,
                max=10,
                message="O telefone precisa conter exatamente 10 números",
            ),
        ],
    )

    zip = StringField(
        "CEP",
        [
            Required("Informe um CEP valido"),
            Length(min=8, max=8, message="O CEP precisa conter exatamente 8 números"),
            Optional(),
            Regexp("^[0-9]*$", message="Informe somente números"),
        ],
    )
    city = StringField("Cidade", [Required("Informe uma cidade")])
    address = StringField(
        "Endereço",
        [
            Required("Informe o endereço"),
            Length(min=1, max=70, message="O endereço pode ter no máximo 70 caracters"),
        ],
    )
    district = StringField(
        "Bairro",
        [
            Required("Informe o bairro"),
        ],
    )

    def load(self, institution):
        self.process(obj=institution)

        if institution.register is not None:
            self.zip.data = institution.register.zip
            self.address.data = institution.register.address
            self.city.data = institution.register.city
            self.district.data = institution.register.district


class FormOrder(BaseForm):
    freight = FloatField("Frete", validators=[Required("O frete é obrigatorio")])
    type_of_sale = QuerySelectField(
        "Tipo de venda",
        validators=[Required("O tipo de venda é obrigatorio!")],
        get_label="type_of_sale",
        get_pk=lambda x: x.id,
        query_factory=lambda: SaleType.query,
        allow_blank=True,
    )
    type_pgto = QuerySelectField(
        "Prazo Pgto.",
        validators=[Required("O prazo do pagamento é obrigatorio!")],
        get_label="type_of_payment",
        get_pk=lambda x: x.id,
        query_factory=lambda: PaymentType.query,
        allow_blank=True,
    )
    discount = FloatField("Desconto")


class FormOrderItems(BaseForm):
    product_id = QuerySelectField(
        "Produto",
        validators=[Required("Selecione o produto para adicionar")],
        get_label="name",
        get_pk=lambda x: x.id,
        query_factory=lambda: Storage.get_avaliable_items(),
        allow_blank=True,
    )
    amount = StringField(
        "Quantidade",
        validators=[
            Required("Informe a quantidade"),
            Regexp("^[0-9]*$", message="Informe somente números"),
        ],
    )


class FormFinishOrder(BaseForm):
    register_id = QuerySelectField(
        "Médico/Instituição",
        validators=[Required("Informe para quem será feita a venda")],
        get_pk=lambda x: x.id,
        query_factory=lambda: Register.query,
        allow_blank=True,
    )
