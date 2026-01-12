from django.forms.widgets import PasswordInput
from django.utils.html import escape
from django.utils.safestring import mark_safe


class PasswordInputFieldWidget(PasswordInput):
    template_name = None

    def render(self, name, value, attrs=None, renderer=None):
        attrs = attrs or {}
        attrs.setdefault('type', 'password')
        attrs.setdefault('name', name)
        attrs.setdefault('id', f'id_{name}')

        final_attrs = {**self.attrs, **attrs}

        base_classes = (
            "inline-block border border-base-200 bg-white font-medium min-w-20 placeholder-base-400 "
            "placeholder-opacity-75 rounded-default shadow-xs text-font-default-light text-sm "
            "focus:outline-2 focus:-outline-offset-2 focus:outline-primary-600 "
            "group-[.errors]:border-red-600 focus:group-[.errors]:outline-red-600 "
            "dark:bg-base-900 dark:border-base-700 dark:text-font-default-dark "
            "dark:placeholder-base-500 dark:group-[.errors]:border-red-500 "
            "dark:focus:group-[.errors]:outline-red-500 dark:scheme-dark "
            "group-[.primary]:border-transparent px-3 py-2 w-full max-w-2xl appearance-none truncate"
        )
        final_attrs['class'] = base_classes

        attr_str = " ".join(f'{key}="{escape(val)}"' for key, val in final_attrs.items())
        html = f"""
            <div id="password-container" class="relative w-full max-w-2xl">
                <input {attr_str} 
                    class="peer border border-base-200 bg-white rounded-default px-3 py-2 w-full text-sm placeholder-base-400 focus:outline-none focus:ring-2 focus:ring-primary-600 dark:bg-base-900 dark:border-base-700 dark:text-font-default-dark dark:placeholder-base-500"
                    placeholder="Enter password"
                />
                <button type="button" 
                    id="togglePassword"
                    class="absolute top-1/2 bottom-1/8 right-2 -translate-y-1/2 flex items-center px-2 text-gray-400 hover:text-gray-600 dark:text-gray-300 dark:hover:text-white"
                    onclick="
                        const input = this.previousElementSibling; 
                        input.type = input.type === 'password' ? 'text' : 'password'; 
                        this.querySelector('span').textContent = input.type === 'password' ? 'visibility' : 'visibility_off';
                    "
                >
                    <span class="material-symbols-outlined">visibility</span>
                </button>
            </div>

        """
        return mark_safe(html)
