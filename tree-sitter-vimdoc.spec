%define     _disable_lto    1
%define     debug_package   %{nil}

%define     tslanguage  vimdoc
%define     libname %mklibname tree-sitter-vimdoc 
%define     devname %mklibname tree-sitter-vimdoc 

Name:       %{libname} 
Version:    3.0.0 
Release:    1
SOURCE0:    https://github.com/neovim/tree-sitter-vimdoc/archive/v%{version}.tar.gz
Summary:    Tree-sitter VIMDOC parser library   
URL:        https://github.com/neovim/tree-sitter-vimdoc
License:    Apache_2.0 
Group:      System/Libraries/C_C++

Provides:   %{libname} = %{EVRD}

%description
Tree-sitter VIMDOC parser library

# ───────────────────────────────────────────────────────────────────────────── #
%package    static 

Summary:    Tree-sitter VIMDOC parser static library 

%description static
Tree-sitter VIMDOC parser static library

# ───────────────────────────────────────────────────────────────────────────── #

%package    devel
Summary:    Development files for %{name}
Requires:   %{libname} = %{EVRD}

%description devel
Development files (Headers etc.) for %{name}

# ───────────────────────────────────────────────────────────────────────────── #
%prep
%setup -c

mv tree-sitter-%{tslanguage}-%{version}/* .


# ───────────────────────────────────────────────────────────────────────────── #

%build
%make_build \
        CC="%{__cc}" \
        CFLAGS="%{optflags}" \
        LDFLAGS="%{build_ldflags}" \
        PREFIX="%{_prefix}" \
        LIBDIR="%{_libdir}" 


# ───────────────────────────────────────────────────────────────────────────── #

%install
%make_install \
        CC="%{__cc}" \
        CFLAGS="%{optflags}" \
        LDFLAGS="%{build_ldflags}" \
        PREFIX="%{_prefix}" \
        LIBDIR="%{_libdir}" 

install -d %{buildroot}%{_libdir}/tree_sitter


libs=$(ls "%{buildroot}%{_libdir}" | \
    sed "/libtree-sitter-%{tslanguage}[^.]*\.so\.[0-9][0-9]*$/!d")

# Create symlink in tree_sitter directory to be used by Neovim  
for lib in $libs; do
    shortname=$(echo "$lib" | sed "s/libtree-sitter-\(%{tslanguage}[^.]*\).*$/\1/")
    ln -s -r "%{buildroot}%{_libdir}/${lib}" \
        "%{buildroot}%{_libdir}/tree_sitter/${shortname}.so"
done



# ───────────────────────────────────────────────────────────────────────────── #

%files 
%{_libdir}/*.so.*
%{_libdir}/tree_sitter/*.so
%license  LICENSE*
%doc README*

# ───────────────────────────────────────────────────────────────────────────── #

%files devel
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*
%license  LICENSE*
%doc    README*

# ───────────────────────────────────────────────────────────────────────────── #

%files static
%{_libdir}/libtree-sitter-vimdoc*.a


