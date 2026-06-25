from django import forms
from .models import Review  # Modelo Review (viene de models/review.py) ⭐

# ─────────────────────────────────────────────
# ⭐ Opciones de estrellas (1 a 5) para el formulario
# ─────────────────────────────────────────────
# Genera una lista de tuplas: [(1, '1'), (2, '2'), ..., (5, '5')]
# Esto se usa para el widget RadioSelect (botones de selección)
STAR_CHOICES = [(opt, str(opt)) for opt in range(1, 6)]

# ─────────────────────────────────────────────
# 📝 Formulario para dejar una RESEÑA / CALIFICACIÓN en un curso
# ─────────────────────────────────────────────
class ReviewForm(forms.ModelForm):
    rating = forms.IntegerField(
        min_value=1, max_value=5,
        widget=forms.RadioSelect(choices=STAR_CHOICES),  # Selector visual de estrellas ⭐
        label="Calificacion"
    )
    comment = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4, 'placeholder': 'Comentario...'}),
        label="Comentario",
        required=False  # 💡 El comentario es OPCIONAL, la estrella es obligatoria
    )

    class Meta:
        model = Review                 # Este formulario guarda en el modelo Review
        fields = ['rating', 'comment'] # Solo estos dos campos

    # ── clean_rating: validación EXTRA del campo rating ──
    # Django ejecuta automáticamente clean_<campo>() cuando se envía el formulario
    def clean_rating(self):
        # Obtenemos el valor que el usuario puso en el campo 'rating'
        rating = self.cleaned_data['rating']

        # ── Evaluamos si está dentro del rango permitido ──
        if not 1 <= rating <= 5:
            # ❌ Fuera de rango -> lanzamos error (Django lo muestra en el template)
            raise forms.ValidationError("La calificación debe estar entre 1 y 5")

        # ✅ Válido -> devolvemos el rating limpio
        return rating

    
