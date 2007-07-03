%{!?_with_external: %{!?_without_external: %define _with_external 1}}

%define gcj_support 1
%define	section	free

Name:		adaptx
Version:	0.9.13
Release:	%mkrel 3.4
Epoch:		0
Summary:	AdaptX
License:	BSD-like
Group:		Development/Java
Source0:	%{name}-%{version}-src-RHCLEAN.tar.bz2
Patch0:		%{name}-%{version}-xsl.patch
Patch1:		%{name}-%{version}-missingstubs.patch
Url:		http://castor.exolab.org/
Requires:	ant >= 0:1.6
Requires:	jpackage-utils >= 0:1.6
Requires:	log4j
Requires:	xml-commons-apis
Requires:	xerces-j2
%if %{?_with_external:1}%{!?_with_external:0}
BuildRequires:	%{name} = %{epoch}:%{version}-%{release}
%endif
BuildRequires:	ant
BuildRequires:	ant-trax
BuildRequires:	java-devel
BuildRequires:	jaxp_transform_impl
BuildRequires:	jpackage-utils >= 0:1.5
BuildRequires:	log4j
BuildRequires:	xerces-j2
BuildRequires:  xml-commons-apis
%if %{gcj_support}
BuildRequires:	java-gcj-compat-devel >= 0:1.0.31
Requires(post):	java-gcj-compat >= 0:1.0.31
Requires(postun): java-gcj-compat >= 0:1.0.31
%else
BuildArch:	noarch
%endif
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

%description
Adaptx is an XSLT processor and XPath engine.

%package javadoc
Group:		Development/Java
Summary:	Javadoc for %{name}

%description javadoc
Javadoc for %{name}.

%package doc
Summary:	Documentation for %{name}
Group:		Development/Java

%description doc
Documentation for %{name}.

%prep
%setup -q -n %{name}-%{version}-src
# remove CVS internal files
for dir in `find . -type d -name CVS`; do rm -rf $dir; done
# remove all binary libs
find . -name "*.jar" -exec rm -f {} \;

%patch0
%patch1

%build
perl -p -i -e 's|classic|modern|' src/build.xml
export OPT_JAR_LIST=
export CLASSPATH=$(build-classpath log4j xerces-j2)
%ant -buildfile src/build.xml jar
%ant -buildfile src/build.xml javadoc
%if %{?_with_external:1}%{!?_with_external:0}
export CLASSPATH=$CLASSPATH:$(build-classpath adaptx xml-commons-apis log4j xerces-j2)
%else
export CLASSPATH=$CLASSPATH:`pwd`/dist/adaptx_%{version}.jar:$(build-classpath xml-commons-apis log4j xerces-j2)
%endif
export OPT_JAR_LIST="ant/ant-trax jaxp_transform_impl"
%ant -buildfile src/build.xml doc

%install
%{__rm} -rf %{buildroot}

# jar
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}
install -m 644 dist/%{name}_%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
(cd $RPM_BUILD_ROOT%{_javadir} && for jar in *-%{version}.jar; do ln -sf ${jar} ${jar/-%{version}/}; done)
# javadoc
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr build/doc/javadoc/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
rm -rf build/doc/javadoc

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{gcj_support}
%post
%{update_gcjdb}

%postun
%{clean_gcjdb}
%endif

%post javadoc
rm -f %{_javadocdir}/%{name}
ln -s %{name}-%{version} %{_javadocdir}/%{name}

%postun javadoc
if [ "$1" = "0" ]; then
    rm -f %{_javadocdir}/%{name}
fi

%files
%defattr(0664,root,root,0755)
%doc src/etc/{CHANGELOG,contributors.html,LICENSE}
%{_javadir}/*
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/*.jar.*
%endif

%files javadoc
%defattr(0664,root,root,0755)
%{_javadocdir}/%{name}-%{version}

%files doc
%defattr(0664,root,root,0755)
%doc build/doc/*


