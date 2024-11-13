package com.br.model;

import java.util.Set;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.OneToMany;

@Entity
public class Disciplina {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long disciplinaId;

    private String nome;

    private String descricao;

    @OneToMany(mappedBy = "disciplina")
    private Set<Topico> topicos;

	public Long getDisciplinaId() {
		return disciplinaId;
	}

	public void setDisciplinaId(Long disciplinaId) {
		this.disciplinaId = disciplinaId;
	}

	public String getNome() {
		return nome;
	}

	public void setNome(String nome) {
		this.nome = nome;
	}

	public String getDescricao() {
		return descricao;
	}

	public void setDescricao(String descricao) {
		this.descricao = descricao;
	}

	public Set<Topico> getTopicos() {
		return topicos;
	}

	public void setTopicos(Set<Topico> topicos) {
		this.topicos = topicos;
	}

    // Getters e Setters
    
}
