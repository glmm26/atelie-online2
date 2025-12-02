// payments.js — masks and validation for checkout fields


(function(){
  'use strict';

  // Helpers
  function setCaretPosition(el, pos) {
    try { el.setSelectionRange(pos, pos); } catch(e) { }
  }

  function luhnCheck(number) {
    var s = String(number).replace(/\D/g, '').split('').reverse().map(Number);
    var sum = 0;
    for (var i = 0; i < s.length; i++) {
      var v = s[i];
      if (i % 2 === 1) v = v * 2;
      if (v > 9) v = v - 9;
      sum += v;
    }
    return (sum % 10) === 0;
  }

  function isValidExp(mmss) {
    if (!mmss || !/^[0-1][0-9]\/?[0-9]{2}$/.test(mmss)) return false;
    var parts = mmss.split('/');
    if (parts.length !== 2) return false;
    var mm = parseInt(parts[0], 10);
    var yy = parseInt(parts[1], 10);
    if (isNaN(mm) || isNaN(yy)) return false;
    if (mm < 1 || mm > 12) return false;
    var now = new Date();
    var year = now.getFullYear() % 100;
    var month = now.getMonth() + 1;
    if (yy < year) return false;
    if (yy === year && mm < month) return false;
    return true;
  }

  function markInvalid(el, msg) {
    if (!el) return;
    el.classList.add('invalid');
    el.setAttribute('aria-invalid','true');
    var existing = el.parentNode.querySelector('.error-msg');
    if (!existing) {
      var span = document.createElement('div');
      span.className = 'error-msg';
      span.textContent = msg || 'Inválido';
      el.parentNode.appendChild(span);
    } else {
      existing.textContent = msg || 'Inválido';
    }
  }

  function clearInvalid(el) {
    if (!el) return;
    el.classList.remove('invalid');
    el.removeAttribute('aria-invalid');
    var existing = el.parentNode.querySelector('.error-msg');
    if (existing) existing.parentNode.removeChild(existing);
  }

  // Masks & etapas
  document.addEventListener('DOMContentLoaded', function(){
    var inputNumber = document.querySelector('.card-number');
    var inputExp = document.querySelector('.card-exp');
    var inputCvv = document.querySelector('.card-cvv');
    var form = document.getElementById('checkout-form');
    var includeDelivery = document.getElementById('include-delivery');
    var deliverySection = document.getElementById('delivery-section');

    // Não há etapas — apenas validação e máscaras para pagamento

    // Máscara cartão
    if (inputNumber) {
      inputNumber.addEventListener('input', function(e){
        var el = e.target;
        var raw = el.value.replace(/\D/g, '').slice(0,19);
        var selectionStart = el.selectionStart || 0;
        var digitsBefore = el.value.slice(0, selectionStart).replace(/\D/g, '').length;
        var parts = [];
        for (var i=0;i<raw.length;i+=4) parts.push(raw.slice(i,i+4));
        var formatted = parts.join(' ');
        if (formatted !== el.value) el.value = formatted;
        var pos = 0, digitCount = 0;
        while (pos < formatted.length && digitCount < digitsBefore) {
          if (/\d/.test(formatted.charAt(pos))) digitCount++;
          pos++;
        }
        if (digitCount < digitsBefore) pos = formatted.length;
        setCaretPosition(el, pos);
        clearInvalid(el);
      });
      inputNumber.addEventListener('blur', function(e){
        var raw = e.target.value.replace(/\D/g, '');
        if (raw.length !== 16) {
          markInvalid(e.target, 'O número do cartão deve ter 16 dígitos');
        } else {
          clearInvalid(e.target);
        }
      });
    }

    // Máscara validade
    if (inputExp) {
      inputExp.addEventListener('input', function(e){
        var v = e.target.value.replace(/\D/g, '').slice(0,4);
        if (v.length >= 3) v = v.slice(0,2) + '/' + v.slice(2);
        e.target.value = v;
        clearInvalid(e.target);
      });
      inputExp.addEventListener('blur', function(e){
        if (!isValidExp(e.target.value)) {
          markInvalid(e.target, 'Validade inválida ou expirada');
        } else clearInvalid(e.target);
      });
    }

    // Máscara CVV
    if (inputCvv) {
      inputCvv.addEventListener('input', function(e){
        var v = e.target.value.replace(/\D/g, '').slice(0,4);
        e.target.value = v;
        clearInvalid(e.target);
      });
      inputCvv.addEventListener('blur', function(e){
        var l = e.target.value.length;
        if (l < 3 || l > 4) markInvalid(e.target, 'CVV inválido'); else clearInvalid(e.target);
      });
    }

    // Form submit guard (apenas validação de pagamento + entrega condicional)
    if (form) {
      form.addEventListener('submit', function(ev){
        console.log('Formulário de checkout: submit disparado');
        var invalid = false;
        // se entrega incluida, validar campos de entrega
        var deliveryIncluded = includeDelivery && includeDelivery.checked;
        if (deliveryIncluded) {
          var entregaCampos = ['entrega-nome','entrega-endereco','entrega-cidade','entrega-estado','entrega-cep'];
          entregaCampos.forEach(function(id){
            var el = document.getElementById(id);
            if (!el || el.value.trim().length < 2) { markInvalid(el, 'Preencha este campo de entrega'); invalid = true; }
          });
        }
        var name = form.querySelector('.card-name');
        if (!name || name.value.trim().length < 2) { markInvalid(name, 'Nome inválido'); invalid = true; }
        var num = form.querySelector('.card-number');
        var raw = num ? num.value.replace(/\D/g, '') : '';
        if (!num || raw.length !== 16) { markInvalid(num, 'O número do cartão deve ter 16 dígitos'); invalid = true; }
        var exp = form.querySelector('.card-exp');
        if (!exp || !isValidExp(exp.value)) { markInvalid(exp, 'Validade inválida'); invalid = true; }
        var cvv = form.querySelector('.card-cvv');
        var cvvlen = cvv ? cvv.value.replace(/\D/g,'').length : 0;
        if (!cvv || cvvlen < 3 || cvvlen > 4) { markInvalid(cvv, 'CVV inválido'); invalid = true; }
        if (invalid) {
          ev.preventDefault();
          var firstInvalid = form.querySelector('.invalid');
          if (firstInvalid) {
            firstInvalid.focus();
            alert('Preencha todos os campos corretamente antes de confirmar o pedido.');
          }
        }
      });
    }

    // Toggle delivery section display when checkbox changes
    if (includeDelivery && deliverySection) {
      includeDelivery.addEventListener('change', function(){
        if (includeDelivery.checked) {
          deliverySection.style.display = '';
        } else {
          // clear any validation and values
          var fields = deliverySection.querySelectorAll('.form-control');
          fields.forEach(function(f){ clearInvalid(f); });
          deliverySection.style.display = 'none';
        }
      });
    }
  });
})();
