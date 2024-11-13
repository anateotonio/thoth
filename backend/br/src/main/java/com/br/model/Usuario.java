package com.br.model;

import java.time.LocalDate;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;

@Entity
public class Usuario {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long usuarioId;
    
    private String nome;
    
    private String email;
    
    private String senha;
    
    private LocalDate dataCadastro;
    
    private String tipoUsuario; // aluno, professor, admin
    
    // Getters e Setters
}
