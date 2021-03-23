from odoo import fields, models, api


class ResCountryEpt(models.Model):
    _name = "res.country.ept2"
    _description = "To store the country data"

    name = fields.Char(string="Country", help="Enter country name", required=True)
    country_code = fields.Char(string="Country Code", help="Enter country code")
    state_ids = fields.One2many(string="States", comodel_name="res.state.ept2", inverse_name="country_id")

    def name_get(self):
        """
        This method is used to display informative data in many2one field as per business requirement.
        e.g.: While creating state list it is required to select appropriate country for the state, in normal case
        only country name is displayed in select list menu, now if we want to display country name followed by its
        code then name_get() method is used.
        :return: list of tuple
        """
        if self.env.context.get('context_view_res_state') == 1:
            # checking if the global context has the key of the particular view to apply the below code to
            # that particular view
            display_name_list = []
            for data in self:
                display_name = ''
                display_name += data.name
                display_name += ' - '
                display_name += data.country_code
                display_name_list.append((data.id, display_name))
            return display_name_list
        else:
            return super(ResCountryEpt, self).name_get()

    @api.model
    def _search(self, args, offset=0, limit=None, order=None, count=False, access_rights_uid=None):
        """
        If we want to achieve search in multiple column at a time then this method is used
        :param args: arguments that is passed to be searched
        :param offset: to skip the no. of records
        :param limit: to limit the records
        :param order: to sort by particular field
        :param count: boolean, if false then returns records and if true then returns record count only
        :param access_rights_uid: checks the access rights for the given uid
        :return: search result
        """
        if args:
            if args[0][0] == 'name':
                domain = ['|']
                domain.append(args[0])
                domain.append(('country_code', 'ilike', args[0][2]))
                args = domain
        return super(ResCountryEpt, self)._search(args, offset, limit, order, count, access_rights_uid)

    _sql_constraints = [
        ('country_code_uniqe', 'unique (country_code)', "Country code already exists !"),
    ]